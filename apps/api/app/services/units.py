# ─────────────────────────────────────────────────────────────────────────────
# SERVICE: Units (Unidades / Filiais)
#
# Toda operação aqui é FILTRADA por organization_id.
# Um usuário da Academia A NUNCA pode ver ou modificar unidades da Academia B.
# Isso é o princípio do multi-tenancy aplicado na camada de serviço.
# ─────────────────────────────────────────────────────────────────────────────

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.unit import Unit
from app.schemas.unit import UnitCreate, UnitUpdate


class UnitService:
    """Lógica de negócio para o módulo de Unidades."""

    @staticmethod
    async def criar(
        db: AsyncSession,
        payload: UnitCreate,
        organization_id: int,  # vem do token JWT, não do body
    ) -> Unit:
        """Cria uma nova unidade vinculada à organização do usuário autenticado.

        O organization_id NUNCA vem do body da requisição — sempre do token JWT.
        Isso garante que um usuário só possa criar unidades na sua organização.

        Args:
            db: Sessão do banco de dados.
            payload: Dados validados pelo schema UnitCreate.
            organization_id: ID da organização do usuário autenticado (do JWT).

        Returns:
            A unidade recém-criada.
        """
        unidade = Unit(
            **payload.model_dump(),
            organization_id=organization_id,
        )
        db.add(unidade)
        await db.commit()
        await db.refresh(unidade)
        return unidade

    @staticmethod
    async def listar(
        db: AsyncSession,
        organization_id: int,
    ) -> list[Unit]:
        """Lista todas as unidades ATIVAS de uma organização.

        O filtro por organization_id garante o isolamento multi-tenant.
        Usuário da Academia A recebe apenas unidades da Academia A.

        Returns:
            Lista de unidades ordenadas por nome.
        """
        resultado = await db.execute(
            select(Unit)
            .where(
                Unit.organization_id == organization_id,
                Unit.is_active == True,
            )
            .order_by(Unit.name)
        )
        return list(resultado.scalars().all())

    @staticmethod
    async def buscar_por_id(
        db: AsyncSession,
        unit_id: int,
        organization_id: int,
    ) -> Unit | None:
        """Busca uma unidade pelo ID, garantindo que pertence à organização.

        Por que incluir organization_id na busca?
        Segurança. Se buscássemos só por unit_id, um usuário malicioso poderia
        adivinhar IDs de outras organizações. Com o filtro duplo, isso é impossível.

        Returns:
            A unidade se encontrada e pertencente à organização, None caso contrário.
        """
        resultado = await db.execute(
            select(Unit).where(
                Unit.id == unit_id,
                Unit.organization_id == organization_id,
            )
        )
        return resultado.scalar_one_or_none()

    @staticmethod
    async def atualizar(
        db: AsyncSession,
        unit_id: int,
        organization_id: int,
        payload: UnitUpdate,
    ) -> Unit | None:
        """Atualiza parcialmente uma unidade (PATCH).

        Apenas os campos enviados são alterados.

        Returns:
            A unidade atualizada, ou None se não encontrada.
        """
        unidade = await UnitService.buscar_por_id(db, unit_id, organization_id)
        if not unidade:
            return None

        dados = payload.model_dump(exclude_unset=True)
        for campo, valor in dados.items():
            setattr(unidade, campo, valor)

        await db.commit()
        await db.refresh(unidade)
        return unidade

    @staticmethod
    async def desativar(
        db: AsyncSession,
        unit_id: int,
        organization_id: int,
    ) -> bool:
        """Desativa uma unidade (soft delete).

        Returns:
            True se desativada, False se não encontrada.
        """
        unidade = await UnitService.buscar_por_id(db, unit_id, organization_id)
        if not unidade:
            return False

        unidade.is_active = False
        await db.commit()
        return True
