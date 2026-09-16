# ─────────────────────────────────────────────────────────────────────────────
# SCHEMAS: Student (Aluno)
#
# Representa um aluno/cliente da academia.
# Atenção: Student ≠ User
#   Student = pessoa que paga mensalidade e treina
#   User    = funcionário que opera o sistema
# ─────────────────────────────────────────────────────────────────────────────

from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.student import Gender, StudentStatus


# ── StudentCreate ─────────────────────────────────────────────────────────────
# Usado no POST /students
# O que o recepcionista preenche ao cadastrar um novo aluno.
class StudentCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=255,
        description="Nome completo do aluno.",
        examples=["João da Silva"],
    )
    email: EmailStr = Field(
        ...,
        description="E-mail do aluno. Será usado para contato e login futuro.",
        examples=["joao@email.com"],
    )
    phone: Optional[str] = Field(
        None,
        max_length=20,
        description="Telefone para contato. Ex: '(11) 99999-0000'",
    )
    cpf: Optional[str] = Field(
        None,
        max_length=14,
        description="CPF do aluno (com ou sem pontuação). Ex: '000.000.000-00'",
    )
    birth_date: Optional[date] = Field(
        None,
        description="Data de nascimento. Formato: YYYY-MM-DD",
        examples=["1995-03-15"],
    )
    gender: Optional[Gender] = Field(
        None,
        description="Gênero do aluno.",
    )
    unit_id: Optional[int] = Field(
        None,
        description="ID da unidade onde o aluno está matriculado.",
    )
    # organization_id NÃO vem do body — vem do token JWT do usuário autenticado.
    # Isso garante que um recepcionista só cadastre alunos na SUA organização.


# ── StudentUpdate ─────────────────────────────────────────────────────────────
# Usado no PATCH /students/{id}
# Atualização parcial — só os campos enviados são alterados.
class StudentUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=20)
    cpf: Optional[str] = Field(None, max_length=14)
    birth_date: Optional[date] = None
    gender: Optional[Gender] = None
    unit_id: Optional[int] = None
    status: Optional[StudentStatus] = Field(
        None,
        description=(
            "Status do aluno: "
            "'active' = ativo, "
            "'inactive' = cancelou, "
            "'frozen' = pausado temporariamente"
        ),
    )
    is_active: Optional[bool] = None


# ── StudentResponse ───────────────────────────────────────────────────────────
# Devolvido nas respostas GET, POST, PATCH.
# Inclui todos os campos — incluindo os gerados pelo banco.
class StudentResponse(BaseModel):
    id: int
    organization_id: int
    unit_id: Optional[int] = None
    name: str
    email: str
    phone: Optional[str] = None
    cpf: Optional[str] = None
    birth_date: Optional[date] = None
    gender: Optional[Gender] = None
    status: StudentStatus
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
