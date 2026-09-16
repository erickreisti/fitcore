# ─────────────────────────────────────────────────────────────────────────────
# SCHEMAS: Unit (Unidade / Filial)
#
# Representa uma filial física de uma academia.
# Exemplo: "Academia Iron Body — Unidade Centro"
#
# Hierarquia:
#   Organization → "Academia Iron Body" (a rede)
#     Unit       → "Unidade Centro"     (filial)
#     Unit       → "Unidade Norte"      (outra filial)
# ─────────────────────────────────────────────────────────────────────────────

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ── UnitCreate ────────────────────────────────────────────────────────────────
# Usado no POST /units
class UnitCreate(BaseModel):
    name: str = Field(
        ...,
        min_length=2,
        max_length=255,
        description="Nome da unidade. Ex: 'Unidade Centro'",
        examples=["Unidade Centro"],
    )
    description: Optional[str] = Field(
        None,
        description="Descrição opcional da unidade.",
    )
    address: Optional[str] = Field(
        None,
        max_length=500,
        description="Endereço completo da unidade.",
        examples=["Rua das Flores, 123 — Centro, São Paulo/SP"],
    )
    phone: Optional[str] = Field(
        None,
        max_length=20,
        description="Telefone direto da unidade.",
    )
    # organization_id NÃO vem do body — vem do token JWT do usuário autenticado.
    # Isso evita que um usuário crie uma unidade em uma organização que não é dele.


# ── UnitUpdate ────────────────────────────────────────────────────────────────
# Usado no PATCH /units/{id}
class UnitUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = None
    address: Optional[str] = Field(None, max_length=500)
    phone: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = None


# ── UnitResponse ──────────────────────────────────────────────────────────────
# Devolvido nas respostas GET, POST, PATCH.
class UnitResponse(BaseModel):
    id: int
    organization_id: int
    name: str
    description: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
