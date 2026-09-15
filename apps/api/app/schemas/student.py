from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

# Base properties (compartilhadas)
class StudentBase(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None
    is_active: Optional[bool] = True

# Schema para criação (recebe na rota POST)
class StudentCreate(StudentBase):
    pass

# Schema para atualização (recebe na rota PUT/PATCH)
# Tudo é opcional porque podemos querer atualizar apenas um campo (ex: só o telefone)
class StudentUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    is_active: Optional[bool] = None

# Schema de resposta (devolvido pela API)
# Adiciona os campos que o banco de dados gera (id, data de criação)
class StudentResponse(StudentBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    # Configuração vital: permite que o Pydantic leia objetos do SQLAlchemy
    model_config = ConfigDict(from_attributes=True)
