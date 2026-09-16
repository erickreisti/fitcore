# ─────────────────────────────────────────────────────────────────────────────
# SCHEMAS: User (Usuário do Sistema / Operador)
#
# Lembre-se: User ≠ Student
#   User    = funcionário que OPERA o sistema (recepcionista, gerente, dono)
#   Student = cliente que paga mensalidade e treina
#
# Por que não há senha aqui?
# O Clerk gerencia a autenticação. Nossa API nunca vê a senha do usuário.
# Só trabalhamos com o ID externo que o Clerk nos dá (external_user_id).
#
# Fluxo de criação de usuário:
#   1. Admin cria conta no Clerk dashboard (ou convida por e-mail)
#   2. Clerk gera um user_id (ex: "user_2abc123def456...")
#   3. Admin chama POST /users com esse user_id + role desejado
#   4. Nossa API vincula esse user_id à organização/unidade correta
# ─────────────────────────────────────────────────────────────────────────────

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.user import UserRole


# ── UserCreate ────────────────────────────────────────────────────────────────
# Usado no POST /users
# Admin está vinculando uma conta do Clerk à organização.
class UserCreate(BaseModel):
    external_user_id: str = Field(
        ...,
        description=(
            "ID do usuário no Clerk. "
            "Formato: 'user_2abc123def456...' "
            "Encontre no Clerk Dashboard → Users."
        ),
        examples=["user_2abc123def456xyz"],
    )
    role: UserRole = Field(
        default=UserRole.RECEPTIONIST,
        description="Papel/permissão do usuário no sistema.",
    )
    unit_id: Optional[int] = Field(
        None,
        description=(
            "ID da unidade onde este usuário trabalha. "
            "Deixar em branco para admins que acessam todas as unidades."
        ),
    )
    # organization_id NÃO vem do body — vem do token JWT do admin autenticado.
    # Isso garante que um admin só possa criar usuários na SUA organização.


# ── UserUpdate ────────────────────────────────────────────────────────────────
# Usado no PATCH /users/{id}
# Admin pode alterar o papel ou a unidade de um usuário.
class UserUpdate(BaseModel):
    role: Optional[UserRole] = Field(
        None,
        description="Novo papel do usuário.",
    )
    unit_id: Optional[int] = Field(
        None,
        description="Nova unidade do usuário. Enviar null para remover vínculo.",
    )
    is_active: Optional[bool] = Field(
        None,
        description="Desativar/reativar acesso do usuário ao sistema.",
    )


# ── UserResponse ──────────────────────────────────────────────────────────────
# Devolvido nas respostas GET, POST, PATCH e em /users/me.
class UserResponse(BaseModel):
    id: int
    external_user_id: str
    organization_id: int
    unit_id: Optional[int] = None
    role: UserRole
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
