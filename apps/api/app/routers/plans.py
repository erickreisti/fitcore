# ─────────────────────────────────────────────────────────────────────────────
# ROUTER: Plans (Planos)
#
# O que este arquivo faz?
# Ele é o "Controlador" da API. Quando o Frontend faz uma requisição 
# (ex: GET /api/v1/plans), é este arquivo que atende. Ele verifica as permissões 
# (ex: "é gerente?") e repassa o trabalho pesado para o Service.
# ─────────────────────────────────────────────────────────────────────────────

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.permissions import require_manager, require_staff
from app.schemas.plan import PlanCreate, PlanResponse, PlanUpdate
from app.schemas.user import UserResponse
from app.services.plans import PlanService

router = APIRouter()


@router.post("/", response_model=PlanResponse, status_code=status.HTTP_201_CREATED)
async def criar_plano(
    payload: PlanCreate,
    db: AsyncSession = Depends(get_db),
    # Apenas gerentes ou admins podem CRIAR planos
    current_user: UserResponse = Depends(require_manager),
):
    return await PlanService.criar(db, payload, current_user.organization_id)


@router.get("/", response_model=list[PlanResponse])
async def listar_planos(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    # Qualquer funcionário (recepcionista, etc) pode LISTAR planos para vender
    current_user: UserResponse = Depends(require_staff),
):
    return await PlanService.listar(db, current_user.organization_id, skip, limit)


@router.get("/{plan_id}", response_model=PlanResponse)
async def buscar_plano(
    plan_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(require_staff),
):
    return await PlanService.buscar_por_id(db, plan_id, current_user.organization_id)


@router.patch("/{plan_id}", response_model=PlanResponse)
async def atualizar_plano(
    plan_id: int,
    payload: PlanUpdate,
    db: AsyncSession = Depends(get_db),
    # Apenas gerentes podem EDITAR planos
    current_user: UserResponse = Depends(require_manager),
):
    return await PlanService.atualizar(db, plan_id, payload, current_user.organization_id)


@router.delete("/{plan_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_plano(
    plan_id: int,
    db: AsyncSession = Depends(get_db),
    # Apenas gerentes podem DELETAR planos
    current_user: UserResponse = Depends(require_manager),
):
    await PlanService.deletar(db, plan_id, current_user.organization_id)
