<div align="center">
  <h1>🏋️‍♂️ FitCore OS</h1>
  <p><strong>O Sistema Operacional Definitivo para Redes de Academias</strong></p>

  <p>
    Uma plataforma SaaS multi-tenant focada em alta performance, inteligência de dados (ETL/Analytics) e escalabilidade. Projetada com arquitetura Serverless, integrações orientadas a eventos e modernização tecnológica.
  </p>

  <p>
    <a href="#-stack-tecnológica">Stack</a> •
    <a href="#-arquitetura-monorepo">Arquitetura</a> •
    <a href="#-roadmap-de-engenharia">Roadmap</a> •
    <a href="#-como-executar-localmente">Setup Local</a>
  </p>

  <div>
    <img src="https://img.shields.io/badge/Status-Em%20Desenvolvimento-22c55e?style=for-the-badge" alt="Status" />
    <img src="https://img.shields.io/badge/Arquitetura-Monorepo-8b5cf6?style=for-the-badge" alt="Arquitetura" />
    <img src="https://img.shields.io/badge/Licença-MIT-blue?style=for-the-badge" alt="License" />
  </div>
</div>

---

## 🎯 Sobre o Projeto

O **FitCore OS** foi idealizado para resolver o problema de fragmentação na gestão de franquias e redes de academias. A plataforma unifica controle de acesso, gestão financeira, retenção de clientes e análise de dados em um único ecossistema seguro e escalável.

O diferencial técnico da plataforma reside em seu isolamento rigoroso de dados (**Multi-tenancy**), processamento de alta performance e arquitetura moderna de nuvem, adequada para servir clientes B2B.

### 🌟 Principais Inovações Técnicas
- **Isolamento Multi-tenant Rigoroso:** Controle de acesso com hierarquia de Organizações e Unidades (RBAC) garantindo que dados fiquem 100% isolados por rede de academias.
- **Autenticação Desacoplada e Segura:** Delegação de identidade para provedor especializado (**Clerk**) com validação criptográfica estrita (JWKS) via middleware nativo no backend.
- **Arquitetura Orientada a Performance:** Backend assíncrono (*FastAPI + asyncpg*) e infraestrutura serverless que permite escalabilidade horizontal quase infinita sob demanda (Scale-to-zero).

---

## 🛠 Stack Tecnológica

Optamos por ferramentas estado-da-arte que garantem segurança corporativa, *Developer Experience* (DX) fluida e excelente desempenho.

### 💻 Frontend (Web)
* **Next.js 15 (App Router):** Renderização híbrida (SSR/RSC) para otimização de requisições e experiência de usuário.
* **TypeScript & Tailwind CSS:** Tipagem estática em toda a base e sistema de design utilitário.
* **React Hook Form + Zod:** Tratamento impecável de formulários complexos e validação *schema-based* no lado do cliente.

### ⚙️ Backend (API REST)
* **FastAPI (Python 3.12+):** Framework web assíncrono para construção de APIs ultrarrápidas, provendo OpenAPI nativo.
* **SQLAlchemy 2.0 (Async) + Alembic:** Mapeamento objeto-relacional robusto e controle preciso de migrações estruturais do banco de dados.
* **Pydantic:** Validação de *payloads* de entrada e *serialization* rigorosa de dados de saída.
* **uv:** O gerenciador de pacotes e ambientes virtuais Python de nova geração, escrito em Rust.

### 🗄️ Infraestrutura e Dados
* **Neon DB (PostgreSQL):** Banco de dados relacional *Serverless* com suporte a *branching*, separando totalmente computação de armazenamento.
* **Clerk:** Provedor de Identidade (IdP) enterprise que tira a complexidade do gerenciamento de JWTs, senhas e sessões do nosso banco de dados.

---

## 📂 Arquitetura (Monorepo)

O projeto adota o padrão de monorepo para garantir coesão, facilitar testes de integração e manter versionamento único do produto.

```text
fitcore/
├── apps/
│   ├── web/                    # 💻 Front-end Next.js (Painel B2B)
│   └── api/                    # ⚙️ Back-end FastAPI
│       ├── app/
│       │   ├── core/           # Autenticação, middlewares e DB config
│       │   ├── models/         # Entidades ORM (SQLAlchemy)
│       │   ├── schemas/        # Contratos Pydantic
│       │   ├── services/       # Regras de Negócio e Tenancy
│       │   └── routers/        # Controladores de Requisição REST
│       ├── alembic/            # Histórico de Migrações do PostgreSQL
│       └── pyproject.toml      # Configuração central de pacotes (uv)
└── infra/                      # (Futuro) IaC / Pipelines CI-CD
```

---

## 🗺️ Roadmap de Engenharia

O desenvolvimento segue uma abordagem ágil (Épicos):

### 🏗️ Fase 1: Core Operacional (🚀 Em Andamento)
- [x] Configuração da Arquitetura do Monorepo e Dependências (uv).
- [x] Modelagem estrutural (PostgreSQL via Neon) com foco em isolamento *Multi-tenant*.
- [x] Integração de Identity Provider (Clerk) e Middleware de validação JWKS.
- [x] API: Módulos de Hierarquia — `Organizations`, `Units` e permissões de `Users`.
- [x] API: Módulo de `Students` (Cadastro e listagem multi-tenant segura).
- [ ] API: Módulos Financeiros — Planos, Matrículas e Histórico de Pagamentos.
- [ ] API: Módulo de Acessos — Catraca e Registro de Presença.
- [ ] Web: Setup inicial, design system e proteção de rotas privadas.
- [ ] Web: Integrações HTTP, dashboards e telas de CRUD completas.

### 📊 Fase 2: Inteligência de Dados (Planejado)
- [ ] Implementação de pipelines ETL para alimentar relatórios.
- [ ] Integração com sistema de BI embutido.

### 🤖 Fase 3: IA Generativa e SaaS Global (Planejado)
- [ ] Assinaturas integradas via Stripe (Plataformização).
- [ ] Modelos de *Machine Learning* focados na previsão de Churn (abandono de alunos).
- [ ] Assistente IA generativo integrado à interface web.

---

## 🚀 Como Executar Localmente

### Pré-requisitos Globais
- **Node.js 20+**
- **Python 3.12+**
- **[uv](https://docs.astral.sh/uv/)** (Substituto ultra-rápido para pip e venv)

### 1. Clonar o Repositório
```bash
git clone https://github.com/erickreisti/fitcore.git
cd fitcore
```

### 2. Configurar a API Backend
Abra seu terminal e acesse a raiz da API:
```bash
cd apps/api
```

Crie as variáveis de ambiente baseadas no exemplo:
```bash
cp .env.example .env
```
> **Nota:** Certifique-se de configurar sua `DATABASE_URL` (Neon) e `CLERK_JWKS_URL` dentro do `.env` recém-criado.

Inicie e rode o ambiente local:
```bash
uv sync                             # Instala dependências e cria o ambiente virtual
uv run alembic upgrade head         # Prepara o schema no seu banco de dados
uv run fastapi dev app/main.py      # Sobe o servidor FastAPI com live-reload
```
Acesse os contratos da API em tempo real (Swagger): [http://localhost:8000/docs](http://localhost:8000/docs)

### 3. Configurar a Interface Web (Em Breve)
Em outro terminal:
```bash
cd apps/web
npm install
npm run dev
```

---

<div align="center">
  <p>Construído por engenheiros para elevar o padrão tecnológico do mercado fitness global.</p>
  <p>&copy; 2026 FitCore OS. Distribuído sob a Licença MIT.</p>
</div>
