from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


# ── Base ──────────────────────────────────────────────────────────────────────
# Campos comuns a todos (criação, edição e leitura)
class PlanBase(BaseModel):
    name: str = Field(..., min_length=2, max_length=100, description="Nome do plano")
    description: str | None = Field(None, description="Descrição dos benefícios")
    price: float = Field(..., ge=0, description="Preço do plano. ge=0 garante que não seja negativo")
    duration_days: int = Field(..., gt=0, description="Duração do plano em dias. gt=0 garante que seja pelo menos 1 dia")
    is_active: bool = True


# ── Criação ───────────────────────────────────────────────────────────────────
# Dados necessários para o frontend criar um plano.
class PlanCreate(PlanBase):
    pass


# ── Atualização ───────────────────────────────────────────────────────────────
# Quando o usuário quiser editar, todos os campos são opcionais.
class PlanUpdate(BaseModel):
    name: str | None = Field(None, min_length=2, max_length=100)
    description: str | None = None
    price: float | None = Field(None, ge=0)
    duration_days: int | None = Field(None, gt=0)
    is_active: bool | None = None


# ── Resposta ──────────────────────────────────────────────────────────────────
# Como o dado sai da nossa API de volta pro frontend
class PlanResponse(PlanBase):
    id: int
    organization_id: int
    created_at: datetime
    updated_at: datetime

    # from_attributes=True é OBRIGATÓRIO.
    # Sem isso, o Pydantic não consegue converter o objeto do SQLAlchemy em JSON.
    model_config = ConfigDict(from_attributes=True)
