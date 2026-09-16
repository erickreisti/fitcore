# ─────────────────────────────────────────────────────────────────────────────
# ROUTER: Units (Unidades / Filiais)
#
# Endpoints disponíveis:
#   POST   /api/v1/units        → Criar unidade (admin ou manager)
#   GET    /api/v1/units        → Listar unidades da minha organização
#   GET    /api/v1/units/{id}   → Buscar unidade específica
#   PATCH  /api/v1/units/{id}   → Atualizar unidade
#   DELETE /api/v1/units/{id}   → Desativar unidade (soft delete)
#
# Multi-tenancy:
#   O organization_id SEMPRE vem do token JWT do usuário autenticado.
#   Usuários só veem e gerenciam as unidades da sua própria organização.
# ─────────────────────────────────────────────────────────────────────────────

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.permissions import require_manager, require_any
from app.models.user import User
from app.schemas.unit import UnitCreate, UnitUpdate, UnitResponse
from app.services.units import UnitService

router = APIRouter(prefix="/units", tags=["Unidades"])


@router.post(
    "/",
    response_model=UnitResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Criar unidade",
)
async def criar_unidade(
    payload: UnitCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_manager),
):
    """Cria uma nova unidade/filial para a organização do usuário autenticado.

    O organization_id é extraído automaticamente do token JWT.
    Admins e managers podem criar unidades.
    """
    return await UnitService.criar(
        db=db,
        payload=payload,
        organization_id=current_user.organization_id,
    )


@router.get(
    "/",
    response_model=list[UnitResponse],
    summary="Listar unidades",
)
async def listar_unidades(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_any),
):
    """Lista todas as unidades ativas da organização do usuário autenticado."""
    return await UnitService.listar(
        db=db,
        organization_id=current_user.organization_id,
    )


@router.get(
    "/{unit_id}",
    response_model=UnitResponse,
    summary="Buscar unidade",
)
async def buscar_unidade(
    unit_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_any),
):
    """Busca uma unidade específica da organização do usuário autenticado."""
    unidade = await UnitService.buscar_por_id(
        db=db,
        unit_id=unit_id,
        organization_id=current_user.organization_id,
    )
    if not unidade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidade não encontrada.",
        )
    return unidade


@router.patch(
    "/{unit_id}",
    response_model=UnitResponse,
    summary="Atualizar unidade",
)
async def atualizar_unidade(
    unit_id: int,
    payload: UnitUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_manager),
):
    """Atualiza parcialmente uma unidade."""
    unidade = await UnitService.atualizar(
        db=db,
        unit_id=unit_id,
        organization_id=current_user.organization_id,
        payload=payload,
    )
    if not unidade:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidade não encontrada.",
        )
    return unidade


@router.delete(
    "/{unit_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Desativar unidade",
)
async def desativar_unidade(
    unit_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_manager),
):
    """Desativa uma unidade (soft delete). Dados são preservados."""
    sucesso = await UnitService.desativar(
        db=db,
        unit_id=unit_id,
        organization_id=current_user.organization_id,
    )
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Unidade não encontrada.",
        )
