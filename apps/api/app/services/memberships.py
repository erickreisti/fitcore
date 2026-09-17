# ─────────────────────────────────────────────────────────────────────────────
# SERVICE: Memberships (Matrículas)
#
# O que este arquivo faz?
# Contém as regras de negócio complexas. O maior destaque aqui é a Segurança: 
# como a matrícula amarra um Aluno, uma Unidade e um Plano, nós garantimos que 
# ninguém tente matricular recursos que pertençam a academias diferentes.
# ─────────────────────────────────────────────────────────────────────────────

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.membership import Membership, MembershipStatus
from app.models.student import Student
from app.models.plan import Plan
from app.models.unit import Unit
from app.schemas.membership import MembershipCreate, MembershipUpdate


class MembershipService:
    """Lógica de negócio para Matrículas."""

    @staticmethod
    async def _verificar_pertencimento(
        db: AsyncSession, model_class, item_id: int, organization_id: int, nome_recurso: str
    ):
        """Verifica se a unidade, aluno ou plano pertencem à mesma academia que está tentando matricular."""
        query = select(model_class).where(
            model_class.id == item_id,
            model_class.organization_id == organization_id
        )
        result = await db.execute(query)
        item = result.scalar_one_or_none()
        if not item:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail=f"{nome_recurso} não encontrado nesta organização."
            )

    @staticmethod
    async def criar(db: AsyncSession, payload: MembershipCreate, organization_id: int) -> Membership:
        # 1. Segurança Máxima: Garantir que o aluno, a unidade e o plano são desta academia.
        # Evita que a Academia A tente matricular o Aluno da Academia B no Plano da Academia C.
        await MembershipService._verificar_pertencimento(db, Student, payload.student_id, organization_id, "Aluno")
        await MembershipService._verificar_pertencimento(db, Unit, payload.unit_id, organization_id, "Unidade")
        await MembershipService._verificar_pertencimento(db, Plan, payload.plan_id, organization_id, "Plano")

        # 2. Criar a matrícula
        nova_matricula = Membership(**payload.model_dump(), organization_id=organization_id)
        db.add(nova_matricula)
        await db.commit()
        await db.refresh(nova_matricula)
        return nova_matricula

    @staticmethod
    async def listar(
        db: AsyncSession, organization_id: int, skip: int = 0, limit: int = 100
    ) -> list[Membership]:
        query = select(Membership).where(Membership.organization_id == organization_id).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def buscar_por_id(db: AsyncSession, membership_id: int, organization_id: int) -> Membership:
        query = select(Membership).where(
            Membership.id == membership_id,
            Membership.organization_id == organization_id
        )
        result = await db.execute(query)
        matricula = result.scalar_one_or_none()
        
        if not matricula:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Matrícula não encontrada.")
        return matricula

    @staticmethod
    async def atualizar(
        db: AsyncSession, membership_id: int, payload: MembershipUpdate, organization_id: int
    ) -> Membership:
        matricula = await MembershipService.buscar_por_id(db, membership_id, organization_id)
        
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(matricula, key, value)
            
        await db.commit()
        await db.refresh(matricula)
        return matricula
