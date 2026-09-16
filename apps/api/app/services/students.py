# ─────────────────────────────────────────────────────────────────────────────
# SERVICE: Students (Alunos)
#
# IMPORTANTE — Multi-tenancy:
# TODA query aqui filtra por organization_id.
# Um usuário da Academia A NUNCA deve ver alunos da Academia B.
# O organization_id sempre vem do token JWT do usuário autenticado,
# nunca do corpo da requisição.
# ─────────────────────────────────────────────────────────────────────────────

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


class StudentService:
    """Lógica de negócio para o módulo de Alunos.

    Todos os métodos recebem organization_id como parâmetro obrigatório.
    Isso garante isolamento multi-tenant: dados de uma academia nunca
    aparecem na listagem de outra.
    """

    @staticmethod
    async def criar(
        db: AsyncSession,
        payload: StudentCreate,
        organization_id: int,  # vem do JWT, não do body
    ) -> Student:
        """Cadastra um novo aluno na academia.

        O organization_id é injetado pelo endpoint a partir do token JWT.
        O aluno sempre pertence à organização do usuário que o está criando.

        Args:
            db: Sessão assíncrona do banco de dados.
            payload: Dados validados pelo schema StudentCreate.
            organization_id: ID da organização (do usuário autenticado via JWT).

        Returns:
            O aluno recém-criado com id e timestamps preenchidos.

        Raises:
            409 Conflict: Se e-mail ou CPF já existirem no sistema.
        """
        aluno = Student(
            **payload.model_dump(),
            organization_id=organization_id,
        )
        db.add(aluno)
        try:
            await db.commit()
            await db.refresh(aluno)
        except IntegrityError:
            # Violação de UNIQUE constraint → email ou CPF duplicado.
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um aluno com este e-mail ou CPF.",
            )
        return aluno

    @staticmethod
    async def listar(
        db: AsyncSession,
        organization_id: int,
    ) -> list[Student]:
        """Retorna todos os alunos ATIVOS de uma organização, ordenados por nome.

        O filtro por organization_id é a linha de defesa principal do multi-tenancy.
        Mesmo que alguém tente manipular a query, o filtro sempre está aqui.

        Returns:
            Lista de alunos ativos da organização.
        """
        resultado = await db.execute(
            select(Student)
            .where(
                Student.organization_id == organization_id,
                Student.is_active == True,
            )
            .order_by(Student.name)
        )
        return list(resultado.scalars().all())

    @staticmethod
    async def buscar_por_id(
        db: AsyncSession,
        student_id: int,
        organization_id: int,
    ) -> Student | None:
        """Busca um aluno pelo ID, garantindo que pertence à organização.

        Por que incluir organization_id?
        Sem esse filtro, um usuário poderia adivinhar IDs de alunos de outras
        academias e acessar dados sensíveis (nome, CPF, e-mail).

        Returns:
            O aluno se encontrado e pertencente à organização, None caso contrário.
        """
        resultado = await db.execute(
            select(Student).where(
                Student.id == student_id,
                Student.organization_id == organization_id,
            )
        )
        return resultado.scalar_one_or_none()

    @staticmethod
    async def atualizar(
        db: AsyncSession,
        student_id: int,
        organization_id: int,
        payload: StudentUpdate,
    ) -> Student | None:
        """Atualiza parcialmente os dados de um aluno (PATCH).

        Apenas os campos enviados pelo cliente são alterados.
        Exemplo: se o cliente manda só {"phone": "99999-0000"},
        apenas o telefone é atualizado — nome, email e outros ficam intactos.

        Returns:
            O aluno atualizado, ou None se não encontrado.
        """
        aluno = await StudentService.buscar_por_id(db, student_id, organization_id)
        if not aluno:
            return None

        dados = payload.model_dump(exclude_unset=True)
        for campo, valor in dados.items():
            setattr(aluno, campo, valor)

        await db.commit()
        await db.refresh(aluno)
        return aluno

    @staticmethod
    async def desativar(
        db: AsyncSession,
        student_id: int,
        organization_id: int,
    ) -> bool:
        """Desativa um aluno (soft delete).

        Por que não deletar?
        Preservamos o histórico para:
        - Relatórios de churn (cancelamentos)
        - Histórico de pagamentos
        - Histórico de presença

        Returns:
            True se desativado com sucesso, False se não encontrado.
        """
        aluno = await StudentService.buscar_por_id(db, student_id, organization_id)
        if not aluno:
            return False

        aluno.is_active = False
        await db.commit()
        return True
