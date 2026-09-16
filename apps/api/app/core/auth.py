# ─────────────────────────────────────────────────────────────────────────────
# AUTH MIDDLEWARE — Integração com Clerk
#
# O que este arquivo faz?
# Define a dependência `get_current_user` que:
#   1. Extrai o token JWT do header Authorization
#   2. Valida o token usando as chaves públicas do Clerk (JWKS)
#   3. Extrai o ID do usuário (external_user_id) do payload do token
#   4. Busca o usuário no nosso banco de dados
#   5. Retorna o objeto User para uso nos endpoints
#
# O que é JWT?
# JSON Web Token — um "bilhete assinado" que prova a identidade do usuário.
# Estrutura: header.payload.signature (separados por pontos)
#   header  → algoritmo de assinatura (RS256)
#   payload → dados do usuário (sub, email, exp...)
#   signature → prova que o Clerk assinou (não foi falsificado)
#
# O que é JWKS?
# JSON Web Key Set — conjunto de chaves públicas que o Clerk disponibiliza.
# Usamos a chave pública para VERIFICAR que o token foi assinado pelo Clerk.
# Não podemos forjar um token sem a chave PRIVADA (que só o Clerk tem).
#
# Por que usamos httpx com cache?
# Buscar as chaves JWKS a cada request seria lento (request HTTP extra).
# Cacheamos as chaves por 1 hora e só buscamos de novo se necessário.
# ─────────────────────────────────────────────────────────────────────────────

import time
from typing import Any

import httpx
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.database import get_db
from app.models.user import User

# ── Extrator de Token ─────────────────────────────────────────────────────────
# HTTPBearer é uma dependência do FastAPI que:
# 1. Lê o header "Authorization: Bearer <token>" automaticamente
# 2. Devolve as credenciais (token) para a nossa função usar
# 3. Retorna 403 automaticamente se o header estiver ausente ou malformado
#
# auto_error=False → não retorna erro automaticamente; deixamos controlar.
bearer_scheme = HTTPBearer(auto_error=False)


# ── Cache de Chaves JWKS ──────────────────────────────────────────────────────
# Armazenamos as chaves em memória para evitar um request HTTP a cada validação.
# _jwks_cache → lista de chaves públicas do Clerk
# _jwks_fetched_at → quando buscamos pela última vez (Unix timestamp)
_jwks_cache: list[dict[str, Any]] = []
_jwks_fetched_at: float = 0.0
JWKS_CACHE_TTL = 3600  # 1 hora em segundos


async def _get_clerk_public_keys() -> list[dict[str, Any]]:
    """Busca e armazena em cache as chaves públicas do Clerk.

    O Clerk disponibiliza suas chaves em um endpoint JWKS público.
    Buscamos essas chaves uma vez por hora para verificar tokens JWT.

    Por que cache?
    → Cada request autenticado precisaria de uma chamada HTTP ao Clerk
    → Com cache, fazemos apenas ~24 chamadas por dia em vez de milhares

    Retorna:
        Lista de chaves JWKS no formato JWK (dicts com "kid", "n", "e", etc.)
    """
    global _jwks_cache, _jwks_fetched_at

    agora = time.time()
    cache_expirado = (agora - _jwks_fetched_at) > JWKS_CACHE_TTL

    if not _jwks_cache or cache_expirado:
        if not settings.CLERK_JWKS_URL:
            # Se CLERK_JWKS_URL não estiver configurada, não podemos validar tokens.
            # Isso acontece em desenvolvimento quando ainda não configurou o Clerk.
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=(
                    "Autenticação não configurada. "
                    "Defina CLERK_JWKS_URL no arquivo .env"
                ),
            )

        async with httpx.AsyncClient() as client:
            resposta = await client.get(settings.CLERK_JWKS_URL, timeout=10.0)
            resposta.raise_for_status()
            dados = resposta.json()

        _jwks_cache = dados.get("keys", [])
        _jwks_fetched_at = agora

    return _jwks_cache


def _decode_clerk_token(token: str, chaves: list[dict]) -> dict[str, Any]:
    """Valida e decodifica um JWT do Clerk.

    O processo de validação:
    1. Lê o header do token para descobrir qual chave usar (kid = key ID)
    2. Encontra a chave correspondente no JWKS
    3. Verifica a assinatura com a chave pública
    4. Verifica se o token não expirou (exp)
    5. Retorna o payload (dados do usuário)

    Args:
        token: O JWT em formato string
        chaves: Lista de chaves JWKS do Clerk

    Returns:
        Payload decodificado com os dados do usuário

    Raises:
        HTTPException 401: Token inválido, expirado ou malformado
    """
    # Primeiro, decodificamos o header sem verificar (para obter o "kid").
    # kid = Key ID — identifica qual das chaves JWKS deve ser usada.
    try:
        header = jwt.get_unverified_header(token)
    except jwt.exceptions.DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: não é um JWT válido.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    kid = header.get("kid")

    # Procuramos a chave com o "kid" correspondente no cache JWKS.
    chave_jwk = None
    for chave in chaves:
        if chave.get("kid") == kid:
            chave_jwk = chave
            break

    if chave_jwk is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: chave de assinatura não encontrada.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Convertemos a chave JWK para o formato que o PyJWT consegue usar.
    try:
        chave_publica = jwt.algorithms.RSAAlgorithm.from_jwk(chave_jwk)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Erro ao processar chave de autenticação.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Decodificamos e validamos o token completamente:
    # - Verifica a assinatura com a chave pública
    # - Verifica o campo "exp" (expiração)
    # - Algoritmo RS256: Clerk usa RSA com SHA-256
    try:
        payload = jwt.decode(
            token,
            chave_publica,
            algorithms=["RS256"],
            options={
                "verify_exp": True,   # rejeita tokens expirados
                "verify_aud": False,  # Clerk não exige audience por padrão
            },
        )
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expirado. Faça login novamente.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token inválido: {str(e)}",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return payload


async def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    """Dependência principal de autenticação.

    Use esta função como dependência do FastAPI para proteger um endpoint:

        @router.get("/dados-secretos")
        async def dados_secretos(current_user: User = Depends(get_current_user)):
            return {"msg": f"Olá, {current_user.id}!"}

    O FastAPI injeta automaticamente o token JWT do header Authorization.
    Esta função valida o token e retorna o objeto User do banco de dados.

    Returns:
        User: objeto do usuário autenticado, com organization_id, role, etc.

    Raises:
        401: Token ausente, inválido ou expirado
        403: Usuário não encontrado no banco ou desativado
    """
    # Verificamos se o token foi enviado no header.
    if not credentials:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciais de autenticação não fornecidas. Use: Authorization: Bearer <token>",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = credentials.credentials

    # Buscamos as chaves públicas do Clerk e validamos o token.
    chaves = await _get_clerk_public_keys()
    payload = _decode_clerk_token(token, chaves)

    # O campo "sub" (subject) do JWT contém o ID do usuário no Clerk.
    # Formato Clerk: "user_2abc123def456..."
    clerk_user_id = payload.get("sub")
    if not clerk_user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido: campo 'sub' ausente.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Buscamos o usuário no NOSSO banco de dados pelo external_user_id.
    # Se não encontrar, o usuário do Clerk não foi vinculado à nossa organização.
    resultado = await db.execute(
        select(User).where(User.external_user_id == clerk_user_id)
    )
    usuario = resultado.scalar_one_or_none()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=(
                "Usuário autenticado no Clerk mas não vinculado ao sistema. "
                "Um administrador precisa cadastrá-lo em POST /api/v1/users."
            ),
        )

    if not usuario.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Conta desativada. Entre em contato com o administrador.",
        )

    return usuario


# ── Atalho para uso opcional ──────────────────────────────────────────────────
# Às vezes queremos tentar autenticar mas não obrigar.
# Ex: endpoint que funciona diferente se autenticado ou não.
async def get_current_user_optional(
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
    db: AsyncSession = Depends(get_db),
) -> User | None:
    """Versão opcional de get_current_user. Retorna None se não autenticado."""
    if not credentials:
        return None
    try:
        return await get_current_user(credentials, db)
    except HTTPException:
        return None
