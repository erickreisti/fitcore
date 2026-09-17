# ─────────────────────────────────────────────────────────────────────────────
# MODEL: Plan (Planos da Academia)
#
# Representa os produtos que a academia vende (Mensal, Anual, Promocional).
# Um plano pertence a UMA organização.
# ─────────────────────────────────────────────────────────────────────────────

from sqlalchemy import Boolean, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class Plan(TimestampMixin, Base):
    """Representa um plano de acesso vendido pela academia."""

    __tablename__ = "plans"

    # ── Chave Primária ────────────────────────────────────────────────────────
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # ── Multi-Tenant ──────────────────────────────────────────────────────────
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    # ── Campos do Plano ───────────────────────────────────────────────────────
    
    # Nome do plano (ex: "Anual VIP")
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    
    # Descrição opcional (ex: "Acesso a todas as unidades")
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    
    # Preço: Usamos Numeric(10, 2) para guardar valores financeiros com 2 casas decimais.
    # Ex: 120.50
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    
    # Duração em dias. Um plano mensal teria 30. Um plano anual teria 365.
    duration_days: Mapped[int] = mapped_column(Integer, nullable=False)
    
    # Se is_active for False, o plano para de aparecer na tela de vendas,
    # mas não excluímos do banco, porque alunos antigos podem ter matrículas nele.
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # ── Relacionamentos ───────────────────────────────────────────────────────
    # Permite acessar `plano.organization` e pegar os dados da academia
    organization = relationship("Organization", back_populates="plans")
    
    # Um plano tem várias matrículas vinculadas a ele.
    memberships = relationship("Membership", back_populates="plan")
