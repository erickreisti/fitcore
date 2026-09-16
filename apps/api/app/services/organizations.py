# ─────────────────────────────────────────────────────────────────────────────
# SERVICE: Organizations
#
# O que é um Service?
# Contém a lógica de negócio relacionada a Organizações.
# O Router (HTTP) chama o Service, que por sua vez usa o banco de dados.
#
# Padrão: Router → Service → Banco de dados
#   Router    → recebe a requisição HTTP, valida schema, devolve resposta
#   Service   → contém a lógica: criar, validar slug único, buscar, etc.
#   Banco     → persiste e consulta os dados
#
# Vantagens de separar em Service:
#   1. Lógica reutilizável (scripts, testes, outros routers)
#   2. Router fica limpo — só HTTP, sem SQL
#   3. Fácil de testar unitariamente (mockamos o banco)
# ─────────────────────────────────────────────────────────────────────────────

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate, OrganizationUpdate


class OrganizationService:
    """Lógica de negócio para o módulo de Organizações."""

    @staticmethod
    async def criar(db: AsyncSession, payload: OrganizationCreate) -> Organization:
        """Cria uma nova organização (academia) no sistema.

        Apenas usuários com papel ADMIN do sistema podem chamar esta operação.
        (A verificação de role é feita no router.)

        Args:
            db: Sessão assíncrona do banco de dados.
            payload: Dados validados pelo schema OrganizationCreate.

        Returns:
            A organização recém-criada com id e timestamps preenchidos.

        Raises:
            409 Conflict: Se o slug já estiver em uso por outra organização.
        """
        org = Organization(**payload.model_dump())
        db.add(org)
        try:
            await db.commit()
            await db.refresh(org)
        except IntegrityError:
            # Violação de UNIQUE constraint → slug duplicado.
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Já existe uma organização com o slug '{payload.slug}'.",
            )
        return org

    @staticmethod
    async def listar(db: AsyncSession) -> list[Organization]:
        """Lista todas as organizações ativas.

        Nota: Este endpoint é administrativo — só deve ser acessado por
        superadmins do sistema FitCore (não por usuários das academias).

        Returns:
            Lista de organizações ordenadas por nome.
        """
        resultado = await db.execute(
            select(Organization)
            .where(Organization.is_active == True)
            .order_by(Organization.name)
        )
        return list(resultado.scalars().all())

    @staticmethod
    async def buscar_por_id(db: AsyncSession, org_id: int) -> Organization | None:
        """Busca uma organização pelo ID.

        Returns:
            A organização se encontrada, None caso contrário.
        """
        resultado = await db.execute(
            select(Organization).where(Organization.id == org_id)
        )
        return resultado.scalar_one_or_none()

    @staticmethod
    async def buscar_por_slug(db: AsyncSession, slug: str) -> Organization | None:
        """Busca uma organização pelo slug.

        O slug é usado em URLs amigáveis: fitcore.com/academia-iron-body/

        Returns:
            A organização se encontrada, None caso contrário.
        """
        resultado = await db.execute(
            select(Organization).where(Organization.slug == slug)
        )
        return resultado.scalar_one_or_none()

    @staticmethod
    async def atualizar(
        db: AsyncSession, org_id: int, payload: OrganizationUpdate
    ) -> Organization | None:
        """Atualiza parcialmente uma organização (PATCH).

        Apenas os campos enviados no payload são alterados.
        exclude_unset=True é o que torna isso possível.

        Returns:
            A organização atualizada, ou None se não encontrada.
        """
        org = await OrganizationService.buscar_por_id(db, org_id)
        if not org:
            return None

        # exclude_unset=True → só os campos que o cliente ENVIOU (não os defaults).
        dados = payload.model_dump(exclude_unset=True)
        for campo, valor in dados.items():
            setattr(org, campo, valor)

        await db.commit()
        await db.refresh(org)
        return org

    @staticmethod
    async def desativar(db: AsyncSession, org_id: int) -> bool:
        """Desativa uma organização (soft delete).

        Não apagamos do banco — preservamos todo o histórico de alunos,
        pagamentos e presença para auditoria e relatórios.

        Returns:
            True se desativada com sucesso, False se não encontrada.
        """
        org = await OrganizationService.buscar_por_id(db, org_id)
        if not org:
            return False

        org.is_active = False
        await db.commit()
        return True
