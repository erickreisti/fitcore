<div align="center">

# 🏋️‍♂️ FitCore

**Plataforma SaaS de gestão para redes de academias**  
Sistema web operacional · Inteligência de dados · IA Generativa

<br/>

[![Next.js](https://img.shields.io/badge/Next.js%2015-000000?style=for-the-badge&logo=nextdotjs&logoColor=white)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![Python](https://img.shields.io/badge/Python%203.12-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL%2016-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)

<br/>

![Status](https://img.shields.io/badge/Status-Em%20Desenvolvimento-22c55e?style=flat-square)
![Licença](https://img.shields.io/badge/Licença-MIT-blue?style=flat-square)
![Arquitetura](https://img.shields.io/badge/Arquitetura-Monorepo-8b5cf6?style=flat-square)

</div>

---

## 📋 Índice

- [Sobre o Projeto](#-sobre-o-projeto)
- [Stack Tecnológica](#-stack-tecnológica)
- [Arquitetura do Monorepo](#-arquitetura-do-monorepo)
- [Como Rodar Localmente](#-como-rodar-localmente)
- [Variáveis de Ambiente](#-variáveis-de-ambiente)
- [Roadmap](#-roadmap)
- [Licença](#-licença)

---

## 💡 Sobre o Projeto

O **FitCore** é um sistema **multi-tenant** desenvolvido para digitalizar e automatizar completamente a operação de redes de academias. A plataforma cobre desde o cadastro de alunos e matrículas até dashboards analíticos avançados, previsão de churn com ML e assistentes de IA generativa.

O projeto é construído em **três fases de evolução progressiva**:

<br/>

| | Fase | Descrição | Status |
|:---:|:---|:---|:---:|
| 🚀 | **Fase 1 — Operacional** | Sistema web core: alunos, planos, matrículas, pagamentos e presença | `Em Dev` |
| 📊 | **Fase 2 — Dados** | Engenharia de dados: integrações, pipelines ETL e dashboards analíticos | `Planejado` |
| 🤖 | **Fase 3 — IA & SaaS** | Multi-tenant completo com ML, IA generativa e cobrança recorrente | `Planejado` |

---

## 🛠 Stack Tecnológica

<details open>
<summary><b>💻 Front-end</b> — <code>apps/web</code></summary>
<br/>

| Tecnologia | Uso |
|:---|:---|
| **Next.js 15** (App Router) | Framework principal com SSR e RSC |
| **TypeScript** | Tipagem estática em todo o projeto |
| **Tailwind CSS** | Estilização utilitária |
| **React Hook Form + Zod** | Formulários e validação de esquemas |

</details>

<details open>
<summary><b>⚙️ Back-end</b> — <code>apps/api</code></summary>
<br/>

| Tecnologia | Uso |
|:---|:---|
| **FastAPI** (Python 3.12+) | Framework de API assíncrona de alta performance |
| **SQLAlchemy** | ORM para modelagem relacional |
| **Alembic** | Controle de migrações do banco de dados |
| **Pydantic** | Validação e serialização de dados |

</details>

<details open>
<summary><b>🗄️ Banco de Dados & Infra</b></summary>
<br/>

| Tecnologia | Uso |
|:---|:---|
| **PostgreSQL 16** | Banco de dados operacional principal |
| **Redis** | Cache e filas de tarefas (Fase 2) |
| **Docker + Docker Compose** | Ambiente de desenvolvimento local isolado |
| **GitHub Actions** | CI/CD automatizado |
| **Vercel** | Deploy do front-end em produção |
| **Cloud Run / ECS** | Deploy da API em produção |
| **Supabase Auth / Clerk** | Autenticação com JWT |

</details>

<details>
<summary><b>📈 Analytics</b> — Fase 2</summary>
<br/>

| Tecnologia | Uso |
|:---|:---|
| **dbt** | Transformações e modelagem SQL |
| **Prefect** | Orquestração de pipelines de dados |
| **Metabase** | Dashboards analíticos embarcados |

</details>

---

## 📂 Arquitetura do Monorepo

```
fitcore/
├── apps/
│   ├── web/                    # 💻 Front-end Next.js
│   │   ├── app/                #    Páginas (App Router)
│   │   ├── components/         #    Componentes reutilizáveis
│   │   ├── lib/                #    Utilitários e clientes HTTP
│   │   ├── hooks/              #    React Hooks customizados
│   │   └── package.json
│   │
│   └── api/                    # ⚙️ Back-end FastAPI
│       ├── app/
│       │   ├── main.py         #    Ponto de entrada
│       │   ├── core/           #    Config, segurança e banco
│       │   ├── modules/        #    Domínios (alunos, planos etc.)
│       │   ├── models/         #    Models SQLAlchemy
│       │   ├── schemas/        #    Schemas Pydantic
│       │   └── services/       #    Regras de negócio
│       ├── tests/
│       ├── pyproject.toml
│       └── Dockerfile
│
├── data/                       # 📊 Engenharia de dados (Fase 2)
│   ├── flows/                  #    Pipelines Prefect
│   ├── dbt/                    #    Transformações SQL
│   └── notebooks/              #    Análises exploratórias
│
├── infra/                      # 🏗️ Infraestrutura
│   ├── docker-compose.yml
│   └── terraform/              #    IaC para produção (Fase 3)
│
├── .github/workflows/          # 🔄 CI/CD GitHub Actions
├── docker-compose.yml
└── README.md
```

---

## 🚀 Como Rodar Localmente

### Pré-requisitos

Certifique-se de ter as seguintes ferramentas instaladas:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Node.js 20+](https://nodejs.org/)
- [Python 3.12+](https://www.python.org/)
- [uv](https://docs.astral.sh/uv/) — Gerenciador de pacotes Python (recomendado)

### 1️⃣ Clone e configure

```bash
git clone https://github.com/seu-usuario/fitcore.git
cd fitcore
```

### 2️⃣ Suba o banco de dados

```bash
docker compose up postgres -d
```

### 3️⃣ Rode a API

```bash
cd apps/api
uv sync
uv run alembic upgrade head      # Aplica as migrações
uv run uvicorn app.main:app --reload
```

> ✅ API disponível em: `http://localhost:8000`
> 📚 Documentação interativa: `http://localhost:8000/docs`

### 4️⃣ Rode o front-end

```bash
cd apps/web
npm install
npm run dev
```

> ✅ Front-end disponível em: `http://localhost:3000`

---

## 🔐 Variáveis de Ambiente

Copie os arquivos de exemplo e preencha com suas credenciais:

```bash
cp apps/api/.env.example apps/api/.env
cp apps/web/.env.example apps/web/.env.local
```

Consulte o arquivo [`.env.example`](./.env.example) na raiz para ver todas as variáveis necessárias.

---

## 🗺️ Roadmap

### 🏗️ Fase 1 — Sistema Operacional

- [x] Estrutura do monorepo configurada
- [ ] Modelagem do banco de dados (PostgreSQL + Alembic)
- [ ] API — Módulo de alunos
- [ ] API — Módulo de planos e matrículas
- [ ] API — Módulo de pagamentos
- [ ] API — Módulo de presença
- [ ] Autenticação JWT (Supabase Auth / Clerk)
- [ ] Web — Layout base e autenticação
- [ ] Web — CRUD de alunos
- [ ] Web — Matrículas e pagamentos
- [ ] Web — Check-in presencial
- [ ] Deploy (Vercel + Cloud Run)

### 📊 Fase 2 — Inteligência de Dados

- [ ] Dashboard analítico com Metabase
- [ ] Pipelines ETL com Prefect
- [ ] Transformações SQL com dbt

### 🤖 Fase 3 — IA & SaaS

- [ ] Previsão de churn com Machine Learning
- [ ] Assistente IA generativa para gestores
- [ ] Multi-tenant com cobrança recorrente

---

## 📄 Licença

Distribuído sob a licença **MIT**. Veja o arquivo [LICENSE](./LICENSE) para mais detalhes.

---

<div align="center">

Feito com ☕ e 💪 — **FitCore** &copy; 2026

</div>
