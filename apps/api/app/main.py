from fastapi import FastAPI

from app.routers import students

# Inicializa o aplicativo FastAPI.
# Os parâmetros abaixo geram a documentação automática em /docs (Swagger) e /redoc.
app = FastAPI(
    title="FitCore API",
    description="API do sistema de gestão para redes de academias",
    version="0.1.0",
)

# ─── Routers ────────────────────────────────────────────────────────────────
# Cada módulo tem seu próprio router. Registramos todos aqui com um prefixo
# de versão (/api/v1) para facilitar futuras migrações sem quebrar clientes.
app.include_router(students.router, prefix="/api/v1")


# ─── Health checks ──────────────────────────────────────────────────────────
@app.get("/health", tags=["Sistema"])
def health():
    """Verifica se o processo está vivo."""
    return {"status": "ok"}


@app.get("/ready", tags=["Sistema"])
def ready():
    """Verifica se a aplicação está pronta para receber requisições."""
    # TODO: adicionar verificação de conexão com o banco
    return {"status": "ready"}
