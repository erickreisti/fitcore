# ─────────────────────────────────────────────────────────────────────────────
# ROUTER: Students (Alunos)
#
# Endpoints disponíveis:
#   POST   /api/v1/students        → Cadastrar novo aluno
#   GET    /api/v1/students        → Listar alunos da organização
#   GET    /api/v1/students/{id}   → Buscar aluno específico
#   PATCH  /api/v1/students/{id}   → Atualizar dados do aluno
#   DELETE /api/v1/students/{id}   → Desativar aluno (soft delete)
#
# Multi-tenancy:
#   O organization_id SEMPRE vem do token JWT — nunca do body.
#   Um recepcionista da Academia A não pode ver os alunos da Academia B.
# ─────────────────────────────────────────────────────────────────────────────

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core.permissions import require_staff, require_any
from app.models.user import User
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse
from app.services.students import StudentService

# APIRouter é como um "mini-FastAPI" para um módulo específico.
# prefix="/students" → todas as rotas começam com /api/v1/students
# tags=["Alunos"]   → agrupa no Swagger (/docs)
router = APIRouter(prefix="/students", tags=["Alunos"])


@router.post(
    "/",
    response_model=StudentResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar aluno",
)
async def criar_aluno(
    payload: StudentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_staff),  # recepcionista+ pode cadastrar
):
    """Cadastra um novo aluno na academia.

    O organization_id é extraído automaticamente do token JWT do usuário.
    O recepcionista não precisa (e não pode) informar a organização manualmente.
    """
    return await StudentService.criar(
        db=db,
        payload=payload,
        organization_id=current_user.organization_id,
    )


@router.get(
    "/",
    response_model=list[StudentResponse],
    summary="Listar alunos",
)
async def listar_alunos(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_any),  # qualquer autenticado pode ver
):
    """Retorna todos os alunos ativos da organização do usuário autenticado."""
    return await StudentService.listar(
        db=db,
        organization_id=current_user.organization_id,
    )


@router.get(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Buscar aluno",
)
async def buscar_aluno(
    student_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_any),
):
    """Retorna os dados de um aluno específico pelo ID."""
    aluno = await StudentService.buscar_por_id(
        db=db,
        student_id=student_id,
        organization_id=current_user.organization_id,
    )
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado.",
        )
    return aluno


@router.patch(
    "/{student_id}",
    response_model=StudentResponse,
    summary="Atualizar aluno",
)
async def atualizar_aluno(
    student_id: int,
    payload: StudentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_staff),
):
    """Atualiza parcialmente os dados de um aluno. Apenas os campos enviados são alterados."""
    aluno = await StudentService.atualizar(
        db=db,
        student_id=student_id,
        organization_id=current_user.organization_id,
        payload=payload,
    )
    if not aluno:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado.",
        )
    return aluno


@router.delete(
    "/{student_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Desativar aluno",
    description="Soft delete: desativa sem apagar o histórico.",
)
async def desativar_aluno(
    student_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_staff),
):
    """Desativa um aluno (soft delete). O registro é mantido no banco para histórico."""
    sucesso = await StudentService.desativar(
        db=db,
        student_id=student_id,
        organization_id=current_user.organization_id,
    )
    if not sucesso:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Aluno não encontrado.",
        )
