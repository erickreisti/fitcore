# ─────────────────────────────────────────────────────────────────────────────
# MODEL: Membership (Matrícula)
#
# É o coração do negócio. Liga um Aluno a um Plano, definindo validade e preço.
# ─────────────────────────────────────────────────────────────────────────────

import enum
from datetime import date

from sqlalchemy import Boolean, Date, Enum, ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


# ── Enum de Status da Matrícula ───────────────────────────────────────────────
class MembershipStatus(str, enum.Enum):
    PENDING   = "pending"   # Aguardando primeiro pagamento
    ACTIVE    = "active"    # Aluno em dia
    EXPIRED   = "expired"   # Data de fim passou e não renovou
    CANCELLED = "cancelled" # Cancelado antes do fim
    FROZEN    = "frozen"    # Matrícula trancada (férias, atestado)


class Membership(TimestampMixin, Base):
    """Representa a matrícula (contrato) de um aluno em um plano."""

    __tablename__ = "memberships"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # ── Chaves Estrangeiras ───────────────────────────────────────────────────
    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id", ondelete="CASCADE"), nullable=False, index=True
    )
    unit_id: Mapped[int] = mapped_column(
        ForeignKey("units.id", ondelete="RESTRICT"), nullable=False, index=True
    )
    student_id: Mapped[int] = mapped_column(
        ForeignKey("students.id", ondelete="CASCADE"), nullable=False, index=True
    )
    plan_id: Mapped[int] = mapped_column(
        ForeignKey("plans.id", ondelete="RESTRICT"), nullable=False, index=True
    )

    # ── Campos do Contrato ────────────────────────────────────────────────────
    
    # Quando começa e quando termina a validade
    start_date: Mapped[date] = mapped_column(Date, nullable=False)
    end_date: Mapped[date] = mapped_column(Date, nullable=False)
    
    # O preço ACORDADO no momento da venda. 
    # Por que ter esse campo se o plano já tem o 'price'?
    # Porque o plano pode subir para R$ 150 amanhã, mas este aluno 
    # tem garantido o valor de R$ 120 por causa de uma promoção ou contrato antigo.
    agreed_price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    
    status: Mapped[MembershipStatus] = mapped_column(
        Enum(MembershipStatus, name="membershipstatus", create_constraint=True),
        default=MembershipStatus.PENDING,
        nullable=False,
    )

    # ── Relacionamentos ───────────────────────────────────────────────────────
    organization = relationship("Organization", back_populates="memberships")
    unit = relationship("Unit", back_populates="memberships")
    student = relationship("Student", back_populates="memberships")
    plan = relationship("Plan", back_populates="memberships")
