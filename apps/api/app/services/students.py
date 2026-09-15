from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.student import Student
from app.schemas.student import StudentCreate, StudentUpdate


class StudentService:
    """Contém toda a lógica de negócio relacionada a Alunos.

    Separar a lógica do router é uma boa prática chamada de "Service Layer".
    Vantagens:
    - O router fica limpo: só recebe e devolve dados HTTP.
    - A lógica pode ser reutilizada em outros contextos (ex: tarefas agendadas, seeds).
    - Fica muito mais fácil escrever testes unitários para a lógica de negócio.
    """

    @staticmethod
    async def criar(db: AsyncSession, payload: StudentCreate) -> Student:
        """Cria um novo aluno no banco de dados.

        O Student(**payload.model_dump()) converte o schema Pydantic em um objeto
        SQLAlchemy, que o banco de dados consegue entender e persistir.
        """
        aluno = Student(**payload.model_dump())
        db.add(aluno)
        try:
            await db.commit()
            # refresh() recarrega o objeto do banco para obter campos gerados
            # automaticamente, como id e created_at.
            await db.refresh(aluno)
        except IntegrityError:
            # IntegrityError ocorre quando violamos uma restrição do banco,
            # como tentar cadastrar um e-mail que já existe (unique=True).
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um aluno com este e-mail.",
            )
        return aluno

    @staticmethod
    async def listar(db: AsyncSession) -> list[Student]:
        """Retorna todos os alunos ativos, ordenados por nome.

        select(Student) monta a query SQL equivalente a:
        SELECT * FROM students WHERE is_active = TRUE ORDER BY name
        """
        resultado = await db.execute(
            select(Student).where(Student.is_active == True).order_by(Student.name)
        )
        # scalars() extrai os objetos Python da resposta bruta do banco.
        # all() transforma em lista.
        return resultado.scalars().all()

    @staticmethod
    async def buscar_por_id(db: AsyncSession, student_id: int) -> Student | None:
        """Busca um aluno pelo ID.

        scalar_one_or_none() retorna o objeto se encontrado, ou None se não existir.
        Nunca lança exceção por ausência de resultado.
        """
        resultado = await db.execute(
            select(Student).where(Student.id == student_id)
        )
        return resultado.scalar_one_or_none()

    @staticmethod
    async def atualizar(
        db: AsyncSession, student_id: int, payload: StudentUpdate
    ) -> Student | None:
        """Atualiza apenas os campos enviados pelo cliente (PATCH parcial).

        exclude_unset=True é a chave do PATCH: retorna apenas os campos
        que foram explicitamente enviados na requisição.
        Exemplo: se o cliente manda {"phone": "99999-0000"}, apenas phone é atualizado.
        Nome e e-mail permanecem intactos.
        """
        aluno = await StudentService.buscar_por_id(db, student_id)
        if not aluno:
            return None

        dados = payload.model_dump(exclude_unset=True)
        for campo, valor in dados.items():
            setattr(aluno, campo, valor)

        await db.commit()
        await db.refresh(aluno)
        return aluno

    @staticmethod
    async def desativar(db: AsyncSession, student_id: int) -> bool:
        """Desativa um aluno (soft delete).

        Não apagamos o registro do banco porque precisamos manter:
        - Histórico de pagamentos vinculados ao aluno.
        - Histórico de presenças.
        - Relatórios de cancelamento e churn.

        Alunos desativados têm is_active=False e não aparecem nas listagens normais.
        """
        aluno = await StudentService.buscar_por_id(db, student_id)
        if not aluno:
            return False

        aluno.is_active = False
        await db.commit()
        return True
