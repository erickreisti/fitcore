# ─────────────────────────────────────────────────────────────────────────────
# MODELO: Organization (Organização / Academia)
#
# O que é este arquivo?
# Define a tabela "organizations" no banco de dados PostgreSQL.
# Esta é a tabela RAIZ de todo o sistema multi-tenant.
#
# Por que "Organization" e não "Academia"?
# Usamos termos genéricos em inglês para que o sistema possa ser usado
# por qualquer tipo de negócio no futuro (clínicas, estúdios, escolas...).
# A Academia em si é representada por uma Organization.
#
# Relação com as outras tabelas:
#
#   Organization (esta tabela)
#   └── Unit (unidades/filiais da academia)
#       ├── Student (alunos matriculados)
#       ├── Membership (matrículas)
#       ├── Payment (pagamentos)
#       └── Attendance (presenças)
#
# Todo registro em QUALQUER tabela do sistema terá um organization_id,
# garantindo que os dados de uma academia nunca se misturem com os de outra.
# ─────────────────────────────────────────────────────────────────────────────

from sqlalchemy import Boolean, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class Organization(TimestampMixin, Base):
    """Representa uma academia (ou rede de academias) no sistema."""

    # Nome da tabela no banco de dados PostgreSQL.
    # Convenção: sempre no plural, minúsculo, em inglês.
    __tablename__ = "organizations"

    # ── Chave Primária ────────────────────────────────────────────────────────
    # Todo registro precisa de um identificador único.
    # index=True → o banco cria um índice para que buscas por id sejam rápidas.
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # ── Campos de Identidade ──────────────────────────────────────────────────

    # Nome comercial da academia. Ex: "Academia Iron Body".
    # String(255) → limita o campo a 255 caracteres (padrão para nomes).
    # nullable=False → campo obrigatório. Não pode cadastrar academia sem nome.
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Slug: versão do nome em formato de URL. Ex: "academia-iron-body".
    # Por que usar slug?
    # → Permite criar URLs amigáveis: fitcore.com/academia-iron-body/dashboard
    # → Serve como identificador legível e único por humanos
    # unique=True → duas organizações não podem ter o mesmo slug.
    # index=True  → buscas por slug serão rápidas (usaremos muito na autenticação).
    slug: Mapped[str] = mapped_column(String(100), unique=True, index=True, nullable=False)

    # Descrição opcional sobre a academia.
    # Text → diferente de String, não tem limite de caracteres (campo livre).
    # Mapped[str | None] → campo opcional, pode ser NULL no banco.
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Informações de Contato ────────────────────────────────────────────────
    # Todas opcionais (Mapped[str | None]) porque podemos cadastrar a organização
    # inicialmente sem todos os dados preenchidos.

    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # ── Controle de Status ────────────────────────────────────────────────────
    # is_active → "soft delete" no nível de organização.
    # Em vez de deletar o registro (e perder todo o histórico de alunos,
    # pagamentos, etc.), apenas desativamos a organização.
    # default=True → toda organização nasce ativa.
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # ── Relacionamentos ORM ───────────────────────────────────────────────────
    # "relationship" não cria colunas no banco — é apenas uma ponte no Python
    # para que possamos acessar os objetos relacionados de forma conveniente.
    #
    # Exemplo de uso:
    #   org = await db.get(Organization, 1)
    #   print(org.units)     → lista todas as unidades desta organização
    #
    # back_populates="organization" → diz ao SQLAlchemy que o lado inverso
    # deste relacionamento está definido em Unit.organization.
    # lazy="selectin" → quando carregarmos uma organização, o SQLAlchemy
    # carrega automaticamente as unidades com uma query separada (mais eficiente
    # em modo async do que o lazy loading padrão).
    users: Mapped[list["User"]] = relationship(
        "User",
        back_populates="organization",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    students: Mapped[list["Student"]] = relationship(
        "Student",
        back_populates="organization",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    plans: Mapped[list["Plan"]] = relationship(
        "Plan",
        back_populates="organization",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    memberships: Mapped[list["Membership"]] = relationship(
        "Membership",
        back_populates="organization",
        cascade="all, delete-orphan",
        lazy="selectin",
    )
    units: Mapped[list["Unit"]] = relationship(
        "Unit",
        back_populates="organization",
        lazy="selectin",
    )

    # created_at e updated_at vêm do TimestampMixin. ✅

    def __repr__(self) -> str:
        # __repr__ define como o objeto aparece quando você usa print() ou
        # o debugger. Muito útil durante o desenvolvimento.
        return f"<Organization id={self.id} name='{self.name}' slug='{self.slug}'>"
