# ─────────────────────────────────────────────────────────────────────────────
# PERMISSIONS — Sistema de Autorização por Papel (RBAC)
#
# O que é RBAC?
# Role-Based Access Control — controle de acesso baseado em papéis.
# Em vez de controlar permissão por usuário (muito trabalhoso),
# definimos PAPÉIS com suas permissões, e atribuímos papéis aos usuários.
#
# Papéis disponíveis (do mais poderoso ao mais restrito):
#   admin       → tudo: criar orgs, unidades, usuários, ver todos os dados
#   manager     → gerenciar sua unidade: alunos, planos, presença, relatórios
#   receptionist→ cadastrar alunos, registrar pagamentos, fazer check-in
#   instructor  → ver alunos e presenças da sua turma (leitura)
#   analyst     → apenas relatórios e dashboards (leitura)
#
# Como usar nos endpoints:
#
#   # Só admins podem criar organizações
#   @router.post("/organizations")
#   async def criar_org(
#       payload: OrganizationCreate,
#       current_user: User = Depends(require_roles(UserRole.ADMIN))
#   ):
#       ...
#
#   # Admins e managers podem listar alunos
#   @router.get("/students")
#   async def listar_alunos(
#       current_user: User = Depends(require_roles(UserRole.ADMIN, UserRole.MANAGER))
#   ):
#       ...
# ─────────────────────────────────────────────────────────────────────────────

from fastapi import Depends, HTTPException, status

from app.core.auth import get_current_user
from app.models.user import User, UserRole


def require_roles(*roles: UserRole):
    """Fábrica de dependências que exige que o usuário tenha um dos papéis.

    Por que "fábrica de dependências"?
    O FastAPI usa o padrão de Dependency Injection (DI).
    Não podemos passar argumentos direto para uma dependência (ex: Depends(require_roles("admin"))).
    Em vez disso, criamos uma FUNÇÃO que retorna a dependência.

    Exemplo de uso:
        # Permite apenas admin
        Depends(require_roles(UserRole.ADMIN))

        # Permite admin OU manager
        Depends(require_roles(UserRole.ADMIN, UserRole.MANAGER))

    Args:
        *roles: Um ou mais UserRole que têm permissão de acessar o endpoint.

    Returns:
        Dependência FastAPI que valida o papel do usuário.
    """
    async def verificar_role(
        current_user: User = Depends(get_current_user),
    ) -> User:
        """Verifica se o usuário autenticado tem um dos papéis requeridos."""
        if current_user.role not in roles:
            # 403 Forbidden → autenticado, mas sem permissão suficiente.
            # Diferença do 401 (Unauthorized):
            #   401 → "não sei quem você é"
            #   403 → "sei quem você é, mas não pode fazer isso"
            nomes_dos_roles = [r.value for r in roles]
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=(
                    f"Acesso negado. "
                    f"Papel necessário: {', '.join(nomes_dos_roles)}. "
                    f"Seu papel: {current_user.role.value}."
                ),
            )
        return current_user

    return verificar_role


# ── Atalhos para os papéis mais comuns ───────────────────────────────────────
# Em vez de escrever `require_roles(UserRole.ADMIN)` em todo lugar,
# criamos atalhos legíveis. Isso melhora muito a leitura dos endpoints.

# Apenas o administrador da rede (dono) pode usar este endpoint.
require_admin = require_roles(UserRole.ADMIN)

# Admins e gerentes de unidade.
require_manager = require_roles(UserRole.ADMIN, UserRole.MANAGER)

# Qualquer funcionário com acesso operacional (não só analistas).
require_staff = require_roles(
    UserRole.ADMIN,
    UserRole.MANAGER,
    UserRole.RECEPTIONIST,
    UserRole.INSTRUCTOR,
)

# Qualquer usuário autenticado pode ver (incluindo analistas).
require_any = require_roles(
    UserRole.ADMIN,
    UserRole.MANAGER,
    UserRole.RECEPTIONIST,
    UserRole.INSTRUCTOR,
    UserRole.ANALYST,
)


def check_same_org(user: User, organization_id: int) -> None:
    """Verifica se o usuário pertence à mesma organização do recurso.

    Multi-tenant: um usuário da Academia A nunca deve ver dados da Academia B.
    Esta função é chamada nos services/routers quando precisamos garantir isso.

    Args:
        user: O usuário autenticado atual.
        organization_id: O organization_id do recurso sendo acessado.

    Raises:
        HTTPException 403: Se o usuário tentar acessar outra organização.
    """
    if user.organization_id != organization_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Acesso negado: você não pertence a esta organização.",
        )
