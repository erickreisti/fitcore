<div align="center">
  <h1>🏋️‍♂️ FitCore OS</h1>
  <p><strong>Gestão de Redes de Academias (SaaS Multi-tenant)</strong></p>

  <p>
    <a href="#-stack-tecnológica">Stack</a> •
    <a href="#-como-rodar-localmente">Setup Local</a> •
    <a href="#-roadmap">Roadmap</a>
  </p>

  <div>
    <img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-22c55e?style=for-the-badge" alt="Status" />
    <img src="https://img.shields.io/badge/Arquitetura-Monorepo-8b5cf6?style=for-the-badge" alt="Arquitetura" />
  </div>
</div>

---

## 🎯 O Projeto

O **FitCore OS** é uma plataforma SaaS projetada para automatizar operações de franquias de academias. 

O grande diferencial do projeto é a arquitetura **Multi-tenant** rigorosa, que garante que diferentes academias (tenants) operem no mesmo sistema com dados 100% isolados, aliados a uma autenticação segura via provedor externo.

## 🛠 Stack Tecnológica

- **Frontend:** Next.js 15, React, TypeScript, Tailwind CSS
- **Backend:** FastAPI, Python 3.12, SQLAlchemy (Async), Alembic, Pydantic, uv
- **Banco de Dados:** PostgreSQL Serverless (Neon DB)
- **Autenticação:** Clerk (Identity Provider com validação JWT/JWKS)

## 📂 Estrutura do Monorepo

```text
fitcore/
├── apps/
│   ├── web/        # Frontend (Painel Administrativo)
│   └── api/        # Backend (API REST Central)
```

## 🚀 Como Rodar Localmente

### 1. Requisitos
- Node.js 20+
- Python 3.12+
- [uv](https://docs.astral.sh/uv/) (Gerenciador ultra-rápido de pacotes Python)

### 2. Rodando a API
```bash
cd apps/api

# Crie e preencha o arquivo .env com sua DATABASE_URL e CLERK_JWKS_URL
cp .env.example .env  

# Instale dependências e crie o banco
uv sync
uv run alembic upgrade head

# Inicie o servidor
uv run fastapi dev app/main.py
```
> Documentação Interativa (Swagger): `http://localhost:8000/docs`

## 🗺️ Roadmap Atual (Etapa 1)

- [x] Configuração Monorepo e Banco de Dados
- [x] Autenticação Segura (Clerk JWT)
- [x] API: Gestão de Organizações, Unidades e Usuários
- [x] API: Gestão Multi-tenant de Alunos
- [ ] API: Módulo de Planos e Pagamentos
- [ ] Web: Setup e Autenticação
- [ ] Web: Telas de CRUD Administrativo

---

<div align="center">
  <p>&copy; 2026 FitCore OS. Todos os direitos reservados.</p>
</div>
