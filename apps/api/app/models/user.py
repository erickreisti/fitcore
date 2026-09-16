# ─────────────────────────────────────────────────────────────────────────────
# MODELO: User (Usuário do Sistema)
#
# O que é este arquivo?
# Define a tabela "users" no banco de dados PostgreSQL.
# Representa um funcionário/operador da academia que tem acesso ao sistema.
#
# ATENÇÃO: Este "User" NÃO é o aluno (Student).
# → Student = pessoa que paga mensalidade e treina na academia
# → User    = pessoa que OPERA o sistema (recepcionista, gerente, dono)
#
# Por que não guardamos a senha aqui?
# A autenticação (login, senha, token) é responsabilidade do Clerk.
# O Clerk cuida de tudo: hash de senha, tokens JWT, sessões, 2FA, recuperação
# de senha, OAuth (Google, GitHub), etc.
# Nossa tabela só precisa saber:
#   1. Qual é o ID deste usuário no Clerk? (external_user_id)
#   2. A qual academia ele pertence? (organization_id)
#   3. Em qual unidade ele trabalha? (unit_id)
#   4. Qual é o seu papel/permissão? (role)
#
# Fluxo de autenticação com Clerk:
#   1. Usuário faz login no front-end (Next.js) via Clerk
#   2. Clerk retorna um JWT (token assinado digitalmente com a chave privada deles)
#   3. O front-end envia esse JWT em TODA requisição para nossa API
#      (header: Authorization: Bearer <token>)
#   4. Nossa API busca a chave pública do Clerk (JWKS endpoint) e valida o JWT
#   5. Extraímos o external_user_id do payload do JWT
#   6. Buscamos esse external_user_id na nossa tabela users
#   7. Retornamos o User completo com organization_id, role, etc.
#   8. A partir daí, filtramos todos os dados por organization_id
#
# Papéis disponíveis (roles):
#   admin       → dono/administrador da rede, acessa tudo
#   manager     → gerente de unidade, acessa dados da sua unidade
#   receptionist→ recepcionista, cadastra alunos e faz check-in
#   instructor  → instrutor, vê presenças e alunos da sua turma
#   analyst     → apenas leitura de relatórios e dashboards
# ─────────────────────────────────────────────────────────────────────────────

import enum

from sqlalchemy import Boolean, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


# ── Enum de Papéis (Roles) ────────────────────────────────────────────────────
# Por que usar Enum em vez de String simples?
#
# Com String, qualquer valor poderia entrar no banco:
#   user.role = "superadmin"   → não existe, mas passaria
#   user.role = "ADMIN"        → diferente de "admin", causaria bugs
#
# Com Enum, o Python e o PostgreSQL validam os valores automaticamente:
#   user.role = "superadmin"   → ValueError imediato
#   user.role = UserRole.ADMIN → correto e tipado
#
# O PostgreSQL cria um tipo ENUM nativo, garantindo integridade no banco.
class UserRole(str, enum.Enum):
    # str como base permite comparar diretamente: role == "admin" → True
    # Isso facilita muito o uso nos endpoints e testes.
    ADMIN        = "admin"
    MANAGER      = "manager"
    RECEPTIONIST = "receptionist"
    INSTRUCTOR   = "instructor"
    ANALYST      = "analyst"


class User(TimestampMixin, Base):
    """Representa um operador do sistema (funcionário da academia)."""

    __tablename__ = "users"

    # ── Chave Primária ────────────────────────────────────────────────────────
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # ── Vínculo com Clerk (Auth Provider) ────────────────────────────────────
    # Este é o ID do usuário no Clerk (formato: "user_2abc123def456...").
    # Clerk gera esse ID automaticamente ao criar a conta do usuário.
    #
    # unique=True → cada conta do Clerk pode estar vinculada a apenas um
    # registro na nossa tabela (relação 1:1 Clerk ↔ nosso User).
    # index=True  → buscamos por este campo em TODA requisição autenticada,
    # então precisa ser muito rápido.
    external_user_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        index=True,
        nullable=False,
    )

    # ── Chaves Estrangeiras (Multi-Tenant) ────────────────────────────────────

    # A qual organização este usuário pertence?
    # nullable=False → todo usuário DEVE pertencer a uma organização.
    organization_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("organizations.id"),
        index=True,
        nullable=False,
    )

    # A qual unidade este usuário está vinculado?
    # nullable=True → pode ser NULL para usuários admin que gerenciam TODAS
    # as unidades (um admin da rede não pertence a uma unidade específica).
    # nullable=False → para recepcionistas e instrutores, sempre terá unidade.
    unit_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("units.id"),
        index=True,
        nullable=True,
    )

    # ── Papel/Permissão ───────────────────────────────────────────────────────
    # Enum(UserRole) → o SQLAlchemy cria o tipo ENUM diretamente no PostgreSQL.
    # Isso significa que o banco rejeita qualquer valor fora do Enum.
    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        nullable=False,
        default=UserRole.RECEPTIONIST,  # papel padrão ao criar um usuário
    )

    # ── Controle de Acesso ────────────────────────────────────────────────────
    # is_active → permite revogar o acesso de um funcionário sem deletar
    # seu histórico de ações no sistema.
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # ── Relacionamentos ORM ───────────────────────────────────────────────────
    # Acesso ao objeto Organization pai deste usuário.
    # Exemplo: user.organization.name → "Academia Iron Body"
    organization: Mapped["Organization"] = relationship(
        "Organization",
        lazy="selectin",
    )

    # Acesso ao objeto Unit (pode ser None se o usuário for admin da rede).
    # Exemplo: user.unit.name → "Unidade Centro" (ou None para admins)
    unit: Mapped["Unit | None"] = relationship(
        "Unit",
        lazy="selectin",
    )

    # created_at e updated_at vêm do TimestampMixin. ✅

    def __repr__(self) -> str:
        return (
            f"<User id={self.id} "
            f"role={self.role.value} "
            f"org_id={self.organization_id}>"
        )
