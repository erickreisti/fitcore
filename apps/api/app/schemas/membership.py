from datetime import date, datetime
from typing import Any
from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.models.membership import MembershipStatus


# ── Base ──────────────────────────────────────────────────────────────────────
class MembershipBase(BaseModel):
    unit_id: int
    student_id: int
    plan_id: int
    start_date: date
    end_date: date
    agreed_price: float = Field(..., ge=0)
    status: MembershipStatus = MembershipStatus.PENDING

    # Validador de nível de modelo (olha para vários campos ao mesmo tempo)
    @model_validator(mode="before")
    @classmethod
    def validate_dates(cls, data: Any) -> Any:
        # Se os dados estiverem num dicionário (criação via JSON)
        if isinstance(data, dict):
            start = data.get("start_date")
            end = data.get("end_date")
            
            # Garante que as datas existam e a data de fim seja depois da data de início
            if start and end and end < start:
                raise ValueError("A data de término (end_date) não pode ser anterior à data de início (start_date).")
                
        return data


# ── Criação ───────────────────────────────────────────────────────────────────
class MembershipCreate(MembershipBase):
    pass


# ── Atualização ───────────────────────────────────────────────────────────────
class MembershipUpdate(BaseModel):
    unit_id: int | None = None
    plan_id: int | None = None
    start_date: date | None = None
    end_date: date | None = None
    agreed_price: float | None = Field(None, ge=0)
    status: MembershipStatus | None = None


# ── Resposta ──────────────────────────────────────────────────────────────────
class MembershipResponse(MembershipBase):
    id: int
    organization_id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
