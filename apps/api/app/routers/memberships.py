# ─────────────────────────────────────────────────────────────────────────────
# ROUTER: Memberships (Matrículas)
#
# O que este arquivo faz?
# Gerencia as rotas HTTP para Matrículas. Usamos a injeção de dependência (Depends) 
# para extrair o usuário logado (current_user) do token JWT, garantindo que 
# saibamos quem está fazendo a ação e de qual academia ele é.
# ─────────────────────────────────────────────────────────────────────────────

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.permissions import require_staff
from app.schemas.membership import MembershipCreate, MembershipResponse, MembershipUpdate
from app.schemas.user import UserResponse
from app.services.memberships import MembershipService

router = APIRouter()


@router.post("/", response_model=MembershipResponse, status_code=status.HTTP_201_CREATED)
async def criar_matricula(
    payload: MembershipCreate,
    db: AsyncSession = Depends(get_db),
    # Qualquer funcionário da academia (recepcionista, etc) pode realizar matrículas
    current_user: UserResponse = Depends(require_staff),
):
    return await MembershipService.criar(db, payload, current_user.organization_id)


@router.get("/", response_model=list[MembershipResponse])
async def listar_matriculas(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(require_staff),
):
    return await MembershipService.listar(db, current_user.organization_id, skip, limit)


@router.get("/{membership_id}", response_model=MembershipResponse)
async def buscar_matricula(
    membership_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(require_staff),
):
    return await MembershipService.buscar_por_id(db, membership_id, current_user.organization_id)


@router.patch("/{membership_id}", response_model=MembershipResponse)
async def atualizar_matricula(
    membership_id: int,
    payload: MembershipUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserResponse = Depends(require_staff),
):
    return await MembershipService.atualizar(db, membership_id, payload, current_user.organization_id)
