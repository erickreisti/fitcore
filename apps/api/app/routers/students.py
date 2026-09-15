from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.schemas.student import StudentCreate, StudentUpdate, StudentResponse
from app.services.students import StudentService

# APIRouter é como um "mini-FastAPI" para um módulo específico.
# prefix="/students" faz todas as rotas daqui começarem com /api/v1/students
# tags=["Alunos"] agrupa as rotas no Swagger (documentação em /docs)
router = APIRouter(prefix="/students", tags=["Alunos"])


# O decorador @router.post define que esta função responde a requisições HTTP POST.
# response_model diz ao FastAPI qual schema usar para serializar a resposta.
# status_code=201 é o código HTTP correto para criação bem-sucedida de recurso.
@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def criar_aluno(payload: StudentCreate, db: AsyncSession = Depends(get_db)):
    """Cadastra um novo aluno na academia."""
    return await StudentService.criar(db, payload)


@router.get("/", response_model=list[StudentResponse])
async def listar_alunos(db: AsyncSession = Depends(get_db)):
    """Retorna a lista de todos os alunos ativos."""
    return await StudentService.listar(db)


# {student_id} é um parâmetro de caminho (path parameter).
# O FastAPI extrai o valor da URL automaticamente e passa para a função.
@router.get("/{student_id}", response_model=StudentResponse)
async def buscar_aluno(student_id: int, db: AsyncSession = Depends(get_db)):
    """Retorna os dados de um aluno específico pelo seu ID."""
    aluno = await StudentService.buscar_por_id(db, student_id)
    if not aluno:
        # HTTPException interrompe o fluxo e devolve um erro HTTP padronizado.
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno


# PATCH é diferente de PUT: aceita atualização parcial (apenas os campos enviados).
# Exemplo: posso mandar só {"phone": "99999-0000"} sem precisar repetir nome e e-mail.
@router.patch("/{student_id}", response_model=StudentResponse)
async def atualizar_aluno(
    student_id: int, payload: StudentUpdate, db: AsyncSession = Depends(get_db)
):
    """Atualiza parcialmente os dados de um aluno. Apenas os campos enviados são alterados."""
    aluno = await StudentService.atualizar(db, student_id, payload)
    if not aluno:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
    return aluno


# Usamos DELETE para desativar, não para apagar fisicamente.
# Isso é chamado de "soft delete": o registro permanece no banco com is_active=False.
# Preservar histórico é importante para relatórios e auditorias.
# status_code=204 significa "sucesso, sem corpo de resposta" — padrão REST para DELETE.
@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def desativar_aluno(student_id: int, db: AsyncSession = Depends(get_db)):
    """Desativa um aluno (soft delete). O registro é mantido no banco para histórico."""
    sucesso = await StudentService.desativar(db, student_id)
    if not sucesso:
        raise HTTPException(status_code=404, detail="Aluno não encontrado")
