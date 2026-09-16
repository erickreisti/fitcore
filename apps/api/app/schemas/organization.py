# ─────────────────────────────────────────────────────────────────────────────
# SCHEMAS: Organization (Organização / Academia)
#
# O que são Schemas?
# São "moldes" de dados usados pelo Pydantic para:
#   1. VALIDAR os dados recebidos nas requisições (body do POST, PATCH, etc.)
#   2. SERIALIZAR os dados das respostas (converter objetos Python em JSON)
#   3. DOCUMENTAR automaticamente a API no Swagger (/docs)
#
# Por que separar em Create / Update / Response?
#   Create   → campos obrigatórios para criação
#   Update   → todos opcionais (PATCH parcial)
#   Response → inclui campos gerados pelo banco (id, created_at, etc.)
#
# Por que não usar o Model SQLAlchemy diretamente?
# O Model SQLAlchemy representa a tabela do banco — tem informações internas
# que não devem vazar para a API (como chaves internas, índices, etc.).
# O Schema é a "interface pública" da API.
# ─────────────────────────────────────────────────────────────────────────────

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ── OrganizationCreate ────────────────────────────────────────────────────────
# Usado no POST /organizations
# O que o cliente precisa enviar para criar uma organização.
class OrganizationCreate(BaseModel):
    # name e slug são obrigatórios — sem eles não faz sentido criar uma org.
    name: str = Field(
        ...,  # ... = obrigatório em Pydantic
        min_length=2,
        max_length=255,
        description="Nome comercial da academia. Ex: 'Academia Iron Body'",
        examples=["Academia Iron Body"],
    )
    slug: str = Field(
        ...,
        min_length=2,
        max_length=100,
        pattern=r"^[a-z0-9]+(?:-[a-z0-9]+)*$",  # só letras, números e hífens
        description="Identificador único na URL. Ex: 'academia-iron-body'",
        examples=["academia-iron-body"],
    )
    description: Optional[str] = Field(
        None,
        description="Descrição opcional sobre a academia.",
    )
    email: Optional[str] = Field(
        None,
        max_length=255,
        description="E-mail de contato da academia.",
    )
    phone: Optional[str] = Field(
        None,
        max_length=20,
        description="Telefone de contato. Ex: '(11) 99999-0000'",
    )


# ── OrganizationUpdate ────────────────────────────────────────────────────────
# Usado no PATCH /organizations/{id}
# TODOS os campos são opcionais — enviamos apenas o que mudou.
# Diferença entre PATCH e PUT:
#   PUT   → substitui o recurso inteiro (precisa enviar tudo)
#   PATCH → atualiza parcialmente (só o que mudou)
class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=2, max_length=255)
    description: Optional[str] = None
    email: Optional[str] = Field(None, max_length=255)
    phone: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = None
    # Nota: slug NÃO está aqui porque mudar o slug quebraria URLs existentes.


# ── OrganizationResponse ──────────────────────────────────────────────────────
# Usado nas respostas de GET, POST, PATCH.
# Inclui TODOS os campos que a API devolve — incluindo os gerados pelo banco.
class OrganizationResponse(BaseModel):
    id: int
    name: str
    slug: str
    description: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime] = None

    # ConfigDict(from_attributes=True) é essencial:
    # Permite que o Pydantic leia objetos SQLAlchemy diretamente.
    # Sem isso, teríamos que converter manualmente cada campo.
    # Exemplo: em vez de Organization.__dict__, o Pydantic lê organization.name
    model_config = ConfigDict(from_attributes=True)
