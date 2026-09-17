# ─────────────────────────────────────────────────────────────────────────────
# MODELO: Student (Aluno)
#
# O que é este arquivo?
# Define a tabela "students" no banco de dados PostgreSQL.
# Representa um aluno/cliente da academia.
#
# IMPORTANTE — Diferença entre Student e User:
#   Student = pessoa que paga mensalidade e TREINA na academia
#   User    = pessoa que OPERA o sistema (recepcionista, gerente, dono)
#
# Multi-tenant:
#   Todo aluno PERTENCE a uma organização (academia) via organization_id.
#   Isso garante que os dados de uma academia nunca apareçam em outra.
#   Exemplo: Academia Iron Body e Academia Power House usam o mesmo sistema,
#   mas os alunos de uma nunca aparecem na listagem da outra.
# ─────────────────────────────────────────────────────────────────────────────

import enum
from datetime import date

from sqlalchemy import Boolean, Date, Enum, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


# ── Enum de Gênero ────────────────────────────────────────────────────────────
# Por que enum e não string?
# Com enum, garantimos que apenas valores válidos entrem no banco.
# Ex: "masculino", "M", "MALE" seriam todos diferentes se fosse string livre.
class Gender(str, enum.Enum):
    MALE        = "male"
    FEMALE      = "female"
    OTHER       = "other"
    PREFER_NOT  = "prefer_not_to_say"


# ── Enum de Status do Aluno ───────────────────────────────────────────────────
# active   → aluno ativo, frequentando normalmente
# inactive → aluno cancelou a matrícula (soft delete)
# frozen   → aluno pausou temporariamente (ex: viagem, lesão)
class StudentStatus(str, enum.Enum):
    ACTIVE   = "active"
    INACTIVE = "inactive"
    FROZEN   = "frozen"


class Student(TimestampMixin, Base):
    """Representa um aluno matriculado em uma academia."""

    __tablename__ = "students"

    # ── Chave Primária ────────────────────────────────────────────────────────
    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    # ── Chaves Estrangeiras (Multi-Tenant) ────────────────────────────────────

    # A qual organização (academia) este aluno pertence?
    # nullable=False → todo aluno DEVE pertencer a uma organização.
    # Isso é a base do multi-tenancy: sem organization_id, sem aluno.
    organization_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("organizations.id"),
        index=True,
        nullable=False,
    )

    # A qual unidade/filial este aluno está matriculado?
    # nullable=True → pode ser None se a academia não tem filiais
    # (algumas academias têm só uma unidade)
    unit_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("units.id"),
        index=True,
        nullable=True,
    )

    # ── Dados Pessoais ────────────────────────────────────────────────────────

    # Nome completo do aluno.
    name: Mapped[str] = mapped_column(String(255), nullable=False)

    # E-mail: único GLOBALMENTE por enquanto.
    # No futuro podemos mudar para único por organização se necessário.
    email: Mapped[str] = mapped_column(
        String(255), unique=True, index=True, nullable=False
    )

    # Telefone: opcional. Nem todo aluno tem ou quer fornecer.
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)

    # CPF: identificador fiscal brasileiro.
    # Opcional porque podemos ter alunos estrangeiros.
    # unique=True → dois alunos não podem ter o mesmo CPF no sistema inteiro.
    cpf: Mapped[str | None] = mapped_column(
        String(14),  # formato: "000.000.000-00" (14 caracteres com pontuação)
        unique=True,
        index=True,
        nullable=True,
    )

    # Data de nascimento: importante para calcular a idade e relatórios.
    # Date → só a data, sem horário (ex: 1995-03-15)
    birth_date: Mapped[date | None] = mapped_column(Date, nullable=True)

    # Gênero: usa o enum Gender definido acima.
    # Mapped[Gender | None] → o campo é opcional.
    gender: Mapped[Gender | None] = mapped_column(
        Enum(Gender),
        nullable=True,
    )

    # ── Status do Aluno ───────────────────────────────────────────────────────
    # Usamos um Enum de status em vez do booleano is_active simples.
    # Por quê? Porque precisamos distinguir "cancelou" de "pausou temporariamente".
    # - ACTIVE   → mensalidade ativa, pode entrar
    # - INACTIVE → cancelou, histórico preservado
    # - FROZEN   → pausou (ex: lesão, viagem) → quando voltar, ativa de novo
    status: Mapped[StudentStatus] = mapped_column(
        Enum(StudentStatus),
        nullable=False,
        default=StudentStatus.ACTIVE,
    )

    # is_active → mantemos para compatibilidade e facilidade de filtros simples.
    # Regra: is_active=True quando status=ACTIVE, False nos demais.
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)

    # ── Relacionamentos ───────────────────────────────────────────────────────
    organization: Mapped["Organization"] = relationship(
        "Organization",
        back_populates="students",
        lazy="selectin",
    )

    unit: Mapped["Unit | None"] = relationship(
        "Unit",
        back_populates="students",
        lazy="selectin",
    )

    memberships: Mapped[list["Membership"]] = relationship(
        "Membership",
        back_populates="student",
        cascade="all, delete-orphan",
        lazy="selectin",
    )

    # created_at e updated_at vêm do TimestampMixin. ✅

    def __repr__(self) -> str:
        return (
            f"<Student id={self.id} "
            f"name='{self.name}' "
            f"org_id={self.organization_id} "
            f"status={self.status.value}>"
        )
