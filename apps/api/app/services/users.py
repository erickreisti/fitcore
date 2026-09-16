# ─────────────────────────────────────────────────────────────────────────────
# SERVICE: Users (Usuários do Sistema / Operadores)
#
# Este service gerencia os funcionários que OPERAM o sistema.
# Não confundir com Student (alunos que treinam na academia).
#
# Integração com Clerk:
# O Clerk gerencia login/senha. Nossa responsabilidade é:
#   - Vincular o ID do Clerk à organização e unidade corretas
#   - Definir o papel (role) do usuário no sistema
#   - Desativar acesso quando necessário
# ─────────────────────────────────────────────────────────────────────────────

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate


class UserService:
    """Lógica de negócio para o módulo de Usuários do sistema."""

    @staticmethod
    async def criar(
        db: AsyncSession,
        payload: UserCreate,
        organization_id: int,  # vem do token JWT do admin, não do body
    ) -> User:
        """Vincula um usuário do Clerk à organização.

        Fluxo esperado:
        1. Admin cria a conta no Clerk Dashboard (ou manda convite por e-mail)
        2. Clerk gera um user_id (ex: "user_2abc123...")
        3. Admin chama este endpoint com o user_id e o role desejado
        4. Nosso sistema vincula esse user_id à organização do admin

        Args:
            db: Sessão do banco de dados.
            payload: Dados do novo usuário (external_user_id, role, unit_id).
            organization_id: ID da organização do admin autenticado (do JWT).

        Returns:
            O usuário recém-criado.

        Raises:
            409 Conflict: Se o external_user_id já estiver vinculado.
        """
        usuario = User(
            **payload.model_dump(),
            organization_id=organization_id,
        )
        db.add(usuario)
        try:
            await db.commit()
            await db.refresh(usuario)
        except IntegrityError:
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=(
                    f"O usuário do Clerk '{payload.external_user_id}' "
                    "já está vinculado ao sistema."
                ),
            )
        return usuario

    @staticmethod
    async def listar(
        db: AsyncSession,
        organization_id: int,
    ) -> list[User]:
        """Lista todos os usuários ATIVOS de uma organização.

        Returns:
            Lista de usuários ordenados por role.
        """
        resultado = await db.execute(
            select(User)
            .where(
                User.organization_id == organization_id,
                User.is_active == True,
            )
            .order_by(User.role)
        )
        return list(resultado.scalars().all())

    @staticmethod
    async def buscar_por_id(
        db: AsyncSession,
        user_id: int,
        organization_id: int,
    ) -> User | None:
        """Busca um usuário pelo ID, garantindo que pertence à organização.

        Returns:
            O usuário se encontrado, None caso contrário.
        """
        resultado = await db.execute(
            select(User).where(
                User.id == user_id,
                User.organization_id == organization_id,
            )
        )
        return resultado.scalar_one_or_none()

    @staticmethod
    async def buscar_por_clerk_id(
        db: AsyncSession,
        external_user_id: str,
    ) -> User | None:
        """Busca um usuário pelo ID externo do Clerk.

        Usado principalmente pelo middleware de autenticação (auth.py).
        Não filtra por organization_id pois o user_id do Clerk é único globalmente.

        Returns:
            O usuário se encontrado, None caso contrário.
        """
        resultado = await db.execute(
            select(User).where(User.external_user_id == external_user_id)
        )
        return resultado.scalar_one_or_none()

    @staticmethod
    async def atualizar(
        db: AsyncSession,
        user_id: int,
        organization_id: int,
        payload: UserUpdate,
    ) -> User | None:
        """Atualiza parcialmente um usuário (role, unit_id, is_active).

        Um admin pode:
        - Mudar o papel de um funcionário
        - Trocar o funcionário de unidade
        - Desativar/reativar o acesso

        Returns:
            O usuário atualizado, ou None se não encontrado.
        """
        usuario = await UserService.buscar_por_id(db, user_id, organization_id)
        if not usuario:
            return None

        dados = payload.model_dump(exclude_unset=True)
        for campo, valor in dados.items():
            setattr(usuario, campo, valor)

        await db.commit()
        await db.refresh(usuario)
        return usuario
