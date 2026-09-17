# ─────────────────────────────────────────────────────────────────────────────
# SERVICE: Plans (Planos)
#
# O que este arquivo faz?
# Aqui mora a "Regra de Negócio". O Service é responsável por injetar o 
# `organization_id` de forma forçada em todas as operações de banco de dados. 
# Isso garante o Multi-tenancy: uma academia nunca vê dados da outra.
# ─────────────────────────────────────────────────────────────────────────────

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.plan import Plan
from app.schemas.plan import PlanCreate, PlanUpdate


class PlanService:
    """Lógica de negócio para Planos."""

    @staticmethod
    async def criar(db: AsyncSession, payload: PlanCreate, organization_id: int) -> Plan:
        # Forçamos o organization_id por segurança
        novo_plano = Plan(**payload.model_dump(), organization_id=organization_id)
        db.add(novo_plano)
        await db.commit()
        await db.refresh(novo_plano)
        return novo_plano

    @staticmethod
    async def listar(
        db: AsyncSession, organization_id: int, skip: int = 0, limit: int = 100
    ) -> list[Plan]:
        # Sempre filtra pela organização
        query = select(Plan).where(Plan.organization_id == organization_id).offset(skip).limit(limit)
        result = await db.execute(query)
        return list(result.scalars().all())

    @staticmethod
    async def buscar_por_id(db: AsyncSession, plan_id: int, organization_id: int) -> Plan:
        query = select(Plan).where(
            Plan.id == plan_id,
            Plan.organization_id == organization_id
        )
        result = await db.execute(query)
        plano = result.scalar_one_or_none()
        
        if not plano:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Plano não encontrado.")
        return plano

    @staticmethod
    async def atualizar(
        db: AsyncSession, plan_id: int, payload: PlanUpdate, organization_id: int
    ) -> Plan:
        plano = await PlanService.buscar_por_id(db, plan_id, organization_id)
        
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(plano, key, value)
            
        await db.commit()
        await db.refresh(plano)
        return plano

    @staticmethod
    async def deletar(db: AsyncSession, plan_id: int, organization_id: int) -> None:
        # Exclusão "física" (hard delete). 
        # Em um cenário real de faturamento, poderíamos apenas fazer um soft-delete (is_active=False).
        plano = await PlanService.buscar_por_id(db, plan_id, organization_id)
        await db.delete(plano)
        await db.commit()
