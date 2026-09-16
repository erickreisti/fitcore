# ─────────────────────────────────────────────────────────────────────────────
# ROUTER: Organizations
#
# Endpoints disponíveis:
#   POST   /api/v1/organizations        → Criar uma nova organização (admin only)
#   GET    /api/v1/organizations        → Listar todas as organizações (admin only)
#   GET    /api/v1/organizations/{id}   → Buscar uma organização específica
#   GET    /api/v1/organizations/slug/{slug} → Buscar por slug
#   PATCH  /api/v1/organizations/{id}   → Atualizar organização
#   DELETE /api/v1/organizations/{id}   → Desativar organização (soft delete)
#
# Segurança:
#   Todos os endpoints requerem autenticação (JWT do Clerk).
#   Criação e desativação exigem papel ADMIN.
# ─────────────────────────────────────────────────────────────────────────────

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.auth import get_current_user
from app.core.permissions import require_admin, require_any
from app.models.user import User
from app.schemas.organization import OrganizationCreate, OrganizationUpdate, OrganizationResponse
from app.services.organizations import OrganizationService

router = APIRouter(prefix="/organizations", tags=["Organizações"])


@router.post(
    "/",
    response_model=OrganizationResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar organização",
    description="Cria uma nova academia/organização. Requer papel ADMIN.",
)
async def criar_organizacao(
    payload: OrganizationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Cadastra uma nova organização no sistema.

    Apenas administradores do sistema FitCore podem criar organizações.
    (Não confundir com admin de uma academia específica.)
    """
    return await OrganizationService.criar(db, payload)


@router.get(
    "/",
    response_model=list[OrganizationResponse],
    summary="Listar organizações",
    description="Lista todas as organizações ativas. Requer autenticação.",
)
async def listar_organizacoes(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Retorna todas as organizações ativas."""
    return await OrganizationService.listar(db)


@router.get(
    "/slug/{slug}",
    response_model=OrganizationResponse,
    summary="Buscar organização por slug",
)
async def buscar_por_slug(
    slug: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_any),
):
    """Busca uma organização pelo slug (ex: 'academia-iron-body')."""
    org = await OrganizationService.buscar_por_slug(db, slug)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Organização com slug '{slug}' não encontrada.",
        )
    return org


@router.get(
    "/{org_id}",
    response_model=OrganizationResponse,
    summary="Buscar organização por ID",
)
async def buscar_organizacao(
    org_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_any),
):
    """Busca uma organização específica pelo ID."""
    org = await OrganizationService.buscar_por_id(db, org_id)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organização não encontrada.",
        )
    return org


@router.patch(
    "/{org_id}",
    response_model=OrganizationResponse,
    summary="Atualizar organização",
)
async def atualizar_organizacao(
    org_id: int,
    payload: OrganizationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Atualiza parcialmente uma organização. Apenas campos enviados são alterados."""
    org = await OrganizationService.atualizar(db, org_id, payload)
    if not org:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organização não encontrada.",
        )
    return org


@router.delete(
    "/{org_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Desativar organização",
    description="Soft delete: desativa sem apagar o histórico.",
)
async def desativar_organizacao(
    org_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_admin),
):
    """Desativa uma organização (soft delete). Dados são preservados."""
    sucesso = await OrganizationService.desativar(db, org_id)
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Organização não encontrada.",
        )
