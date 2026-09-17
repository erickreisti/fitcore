# ─────────────────────────────────────────────────────────────────────────────
# MODELO: Unit (Unidade / Filial)
#
# O que é este arquivo?
# Define a tabela "units" no banco de dados PostgreSQL.
# Representa uma unidade física de uma academia. Ex: "Unidade Centro",
# "Unidade Zona Sul", "Unidade Shopping".
#
# Por que Units existem separadas de Organization?
# Uma rede de academias (Organization) pode ter várias filiais (Units).
# Cada filial tem seu próprio endereço e pode ter seus próprios alunos,
# instrutores e horários.
#
# Hierarquia:
#   Organization → "Academia Iron Body" (a rede como um todo)
#     Unit       → "Unidade Centro"     (filial específica)
#     Unit       → "Unidade Norte"      (outra filial)
#     Unit       → "Unidade Shopping"   (outra filial)
#
# Relação com multi-tenant:
# Além de organization_id, muitas entidades também terão unit_id,
# permitindo filtrar dados por filial dentro de uma organização.
# ─────────────────────────────────────────────────────────────────────────────

from sqlalchemy import Boolean, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class Unit(TimestampMixin, Base):
    """Representa uma unidade/filial de uma academia."""

    __tablename__ = "units"

    # ── Chave Primária ────────────────────────────────────────────────────────
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # ── Chave Estrangeira (Foreign Key) ───────────────────────────────────────
    # ForeignKey("organizations.id") → cria um vínculo com a tabela organizations.
    # Isso garante INTEGRIDADE REFERENCIAL: o banco de dados IMPEDE que você
    # crie uma unidade com um organization_id que não existe.
    #
    # Exemplo do que o banco impede automaticamente:
    #   INSERT INTO units (organization_id, name) VALUES (999, 'Filial X')
    #   → ERRO: organization_id 999 não existe na tabela organizations
    #
    # index=True → buscas por organization_id serão rápidas.
    # nullable=False → toda unidade DEVE pertencer a uma organização.
    organization_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("organizations.id"),
        index=True,
        nullable=False,
    )

    # ── Campos de Identidade ──────────────────────────────────────────────────
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # Descrição opcional da unidade.
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # ── Endereço ──────────────────────────────────────────────────────────────
    # Mantemos o endereço simples por enquanto (um campo de texto).
    # Em uma versão futura, poderíamos separar em rua, número, CEP, cidade...
    # mas isso seria over-engineering para a Fase 1.
    address: Mapped[str | None] = mapped_column(String(500), nullable=True)

    # Telefone direto da unidade (diferente do telefone geral da organização).
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # ── Controle de Status ────────────────────────────────────────────────────
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # ── Relacionamentos ORM ───────────────────────────────────────────────────
    # Lado inverso do relacionamento definido em Organization.units.
    # organization → nos dá acesso ao objeto Organization pai desta Unit.
    #
    # Exemplo de uso:
    #   unit = await db.get(Unit, 1)
    #   print(unit.organization.name)  → "Academia Iron Body"
    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="units",
    )

    # Usuários (recepcionistas, instrutores) alocados nesta unidade
    users: Mapped[list["User"]] = relationship("User", back_populates="unit")

    # Alunos alocados nesta unidade
    students: Mapped[list["Student"]] = relationship("Student", back_populates="unit")

    # Matrículas que ocorrem nesta unidade
    memberships: Mapped[list["Membership"]] = relationship("Membership", back_populates="unit")

    # created_at e updated_at vêm do TimestampMixin. ✅

    def __repr__(self) -> str:
        return f"<Unit id={self.id} name='{self.name}' org_id={self.organization_id}>"
