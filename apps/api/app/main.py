# ─────────────────────────────────────────────────────────────────────────────
# MAIN — Ponto de entrada da API FitCore
#
# O que este arquivo faz?
# 1. Cria a aplicação FastAPI com suas configurações
# 2. Registra todos os routers (cada módulo tem o seu)
# 3. Define os health check endpoints (/health e /ready)
#
# Como o FastAPI processa uma requisição:
#   Cliente → /api/v1/students → main.py encontra o router → students.py cuida
#   main.py é como um "hub central" que conhece todos os módulos.
# ─────────────────────────────────────────────────────────────────────────────

from fastapi import FastAPI
from sqlalchemy import text

from app.core.config import settings
from app.core.database import SessionLocal
from app.routers import organizations, students, units, users, plans, memberships

# ── Criação da Aplicação ──────────────────────────────────────────────────────
# Os parâmetros abaixo aparecem na documentação automática em /docs e /redoc.
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=(
        "API do FitCore — sistema de gestão para redes de academias.\n\n"
        "## Autenticação\n"
        "Use o botão **Authorize** acima e cole seu token JWT do Clerk.\n"
        "Formato: `Bearer <seu_token>`\n\n"
        "## Multi-tenancy\n"
        "Todos os dados são isolados por organização. "
        "Você só vê dados da sua academia."
    ),
    version=settings.VERSION,
)


# ── Registro de Routers ───────────────────────────────────────────────────────
# Cada módulo tem seu próprio router registrado aqui com o prefixo /api/v1.
# Isso facilita versionamento futuro: quando lançarmos a v2, basta registrar
# os novos routers com /api/v2 sem quebrar clientes que usam /api/v1.

app.include_router(organizations.router, prefix="/api/v1")
app.include_router(units.router, prefix="/api/v1")
app.include_router(users.router, prefix="/api/v1")
app.include_router(students.router, prefix=f"{settings.API_V1_STR}/students", tags=["Alunos"])

# Rotas Módulo Financeiro e Contratual
app.include_router(plans.router, prefix=f"{settings.API_V1_STR}/plans", tags=["Planos"])
app.include_router(memberships.router, prefix=f"{settings.API_V1_STR}/memberships", tags=["Matrículas"])


# ── Health Checks ─────────────────────────────────────────────────────────────
# Health checks são endpoints que monitoramento (Railway, Render, etc.) usam
# para saber se a aplicação está funcionando.
#
# Diferença entre /health e /ready:
#   /health → "O processo está vivo?" (rápido, sem I/O)
#              Verifica se o código está rodando sem crashes.
#   /ready  → "A aplicação está pronta para servir requests?" (mais completo)
#              Verifica se as dependências (banco de dados) estão acessíveis.
#
# Por que isso importa no deploy?
# O Railway/Render reinicializa o container se /health retornar erro.
# Eles esperam /ready ficar disponível antes de enviar tráfego real.

@app.get("/health", tags=["Sistema"])
def health():
    """Verifica se o processo está vivo. Rápido, sem dependências externas."""
    return {"status": "ok", "version": settings.VERSION}


@app.get("/ready", tags=["Sistema"])
async def ready():
    """Verifica se a aplicação está pronta — testa a conexão com o banco.

    Por que async?
    Verificar o banco é uma operação I/O (entrada/saída).
    Com async, não bloqueamos outras requisições enquanto esperamos o banco.

    Retorna:
        200 OK → banco acessível, tudo pronto
        503 Service Unavailable → banco inacessível (problema de conexão)
    """
    try:
        # Criamos uma sessão temporária APENAS para testar a conexão.
        async with SessionLocal() as session:
            # "SELECT 1" é a query mais simples possível — só verifica se o banco responde.
            await session.execute(text("SELECT 1"))
        return {"status": "ready", "database": "connected"}
    except Exception as e:
        # Se o banco não responder, retornamos 503 (Service Unavailable).
        # Plataformas de deploy usam esse status para saber que algo está errado.
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Banco de dados inacessível: {str(e)}",
        )
