# FitCore — API

Back-end do sistema FitCore, construído com **FastAPI** e **Python 3.12**.

Responsável por toda a lógica de negócio, validação de dados e comunicação com o banco PostgreSQL.

---

## Tecnologias

| Tecnologia | Versão | Para quê |
|---|---|---|
| Python | 3.12 | Linguagem principal |
| FastAPI | 0.141+ | Framework da API |
| SQLAlchemy | 2.x | ORM async (Python ↔ PostgreSQL) |
| Pydantic v2 | 2.x | Validação de dados e schemas |
| Alembic | 1.20+ | Migrações do banco de dados |
| asyncpg | 0.31+ | Driver PostgreSQL assíncrono |
| uv | — | Gerenciador de dependências |

---

## Estrutura

```
app/
├── core/
│   ├── config.py      # lê variáveis do .env
│   └── database.py    # conexão com o PostgreSQL
├── models/            # tabelas do banco (SQLAlchemy)
├── schemas/           # validação de dados (Pydantic)
├── routers/           # rotas HTTP (FastAPI)
├── services/          # lógica de negócio
└── main.py            # ponto de entrada da API
alembic/               # histórico de migrações do banco
tests/                 # testes automatizados
```

---

## Como rodar localmente

### 1. Pré-requisitos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/) instalado
- PostgreSQL rodando (ou via Docker)

### 2. Instalar dependências

```bash
uv sync
```

### 3. Configurar variáveis de ambiente

Copie o arquivo de exemplo e preencha com seus dados:

```bash
cp ../../.env.example .env
```

Edite o `.env`:

```env
DATABASE_URL=postgresql+asyncpg://usuario:senha@localhost:5432/fitcore
```

### 4. Criar as tabelas no banco

```bash
uv run alembic upgrade head
```

### 5. Iniciar o servidor

```bash
uv run uvicorn app.main:app --reload
```

A API estará disponível em:

| URL | O que é |
|---|---|
| http://localhost:8000 | API |
| http://localhost:8000/docs | Swagger (documentação interativa) |
| http://localhost:8000/redoc | ReDoc (documentação alternativa) |
| http://localhost:8000/health | Health check |

---

## Endpoints disponíveis

### Alunos
| Método | Rota | Descrição |
|---|---|---|
| `POST` | `/api/v1/students` | Cadastrar aluno |
| `GET` | `/api/v1/students` | Listar alunos |
| `GET` | `/api/v1/students/{id}` | Buscar aluno por ID |
| `PATCH` | `/api/v1/students/{id}` | Atualizar aluno |
| `DELETE` | `/api/v1/students/{id}` | Desativar aluno |

---

## Migrações com Alembic

Quando você alterar um model (tabela), gere uma migration:

```bash
# Gerar migration automaticamente com base nos models
uv run alembic revision --autogenerate -m "descricao da mudanca"

# Aplicar as migrations pendentes
uv run alembic upgrade head

# Ver histórico de migrations
uv run alembic history

# Reverter a última migration
uv run alembic downgrade -1
```

---

## Testes

```bash
uv run pytest
```
