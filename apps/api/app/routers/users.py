# ─────────────────────────────────────────────────────────────────────────────
# ROUTER: Users (Usuários do Sistema / Operadores)
#
# Endpoints disponíveis:
#   POST   /api/v1/users        → Vincular usuário Clerk à organização (admin)
#   GET    /api/v1/users        → Listar usuários da organização (admin/manager)
#   GET    /api/v1/users/me     → Retorna meus próprios dados (qualquer autenticado)
#   GET    /api/v1/users/{id}   → Buscar usuário específico (admin/manager)
#   PATCH  /api/v1/users/{id}   → Atualizar papel/unidade (admin)
#
# Nota sobre /users/me:
#   Este endpoint é crucial para o frontend. Assim que o usuário faz login,
#   o frontend chama /users/me para saber qual é o papel dele e quais telas mostrar.
# ─────────────────────────────────────────────────────────────────────────────

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.auth import get_current_user
from app.core.permissions import require_admin, require_manager
from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.users import UserService

router = APIRouter(prefix="/users", tags=["Usuários"])


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Meus dados",
    description="Retorna os dados do usuário autenticado atual.",
)
async def meus_dados(
    current_user: User = Depends(get_current_user),
):
    """Retorna os dados do usuário que está fazendo a requisição.

    Por que este endpoint é tão importante?
    Após o login via Clerk, o frontend não sabe qual é o papel (role) do usuário.
    Ele chama /users/me para descobrir:
      - organization_id → qual academia gerenciar
      - role            → quais menus/telas mostrar
      - unit_id         → qual filial o usuário gerencia
    """
    return current_user


@router.post(
    "/",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Vincular usuário Clerk",
    description="Vincula um usuário do Clerk à organização. Requer papel ADMIN.",
)
async def vincular_usuario(
    payload: UserCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Vincula uma conta do Clerk à organização do admin autenticado.

    Fluxo:
    1. Admin cria conta no Clerk (ou manda convite por e-mail)
    2. Clerk gera um user_id ("user_2abc123...")
    3. Admin chama este endpoint com esse user_id e o role desejado
    4. O sistema vincula o usuário à organização do admin
    """
    return await UserService.criar(
        db=db,
        payload=payload,
        organization_id=current_user.organization_id,
    )


@router.get(
    "/",
    response_model=list[UserResponse],
    summary="Listar usuários da organização",
)
async def listar_usuarios(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_manager),
):
    """Lista todos os usuários ativos da organização do usuário autenticado."""
    return await UserService.listar(
        db=db,
        organization_id=current_user.organization_id,
    )


@router.get(
    "/{user_id}",
    response_model=UserResponse,
    summary="Buscar usuário",
)
async def buscar_usuario(
    user_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_manager),
):
    """Busca um usuário específico da organização."""
    usuario = await UserService.buscar_por_id(
        db=db,
        user_id=user_id,
        organization_id=current_user.organization_id,
    )
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado.",
        )
    return usuario


@router.patch(
    "/{user_id}",
    response_model=UserResponse,
    summary="Atualizar usuário",
    description="Atualiza papel, unidade ou status de um usuário. Requer ADMIN.",
)
async def atualizar_usuario(
    user_id: int,
    payload: UserUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Atualiza role, unit_id ou is_active de um usuário da organização."""
    usuario = await UserService.atualizar(
        db=db,
        user_id=user_id,
        organization_id=current_user.organization_id,
        payload=payload,
    )
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Usuário não encontrado.",
        )
    return usuario
