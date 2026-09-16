from pydantic_settings import BaseSettings, SettingsConfigDict


# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURAÇÕES DA APLICAÇÃO
#
# O que é este arquivo?
# Centraliza TODAS as configurações da API em um único lugar.
# Usamos o Pydantic Settings para:
#   1. Ler variáveis de ambiente do arquivo .env
#   2. Validar que os valores têm o tipo correto (ex: str, int, bool)
#   3. Falhar imediatamente na inicialização se uma config obrigatória estiver
#      faltando — melhor do que descobrir o erro em tempo de execução.
#
# Como usar em outros arquivos:
#   from app.core.config import settings
#   print(settings.DATABASE_URL)
# ─────────────────────────────────────────────────────────────────────────────


class Settings(BaseSettings):
    # ── Informações do Projeto ────────────────────────────────────────────────
    # Valores com padrão — aparecem na documentação Swagger em /docs.
    PROJECT_NAME: str = "FitCore API"
    VERSION: str = "0.1.0"

    # ── Banco de Dados ────────────────────────────────────────────────────────
    # Obrigatório: sem essa variável no .env, a aplicação não inicia.
    # Formato: postgresql+asyncpg://usuario:senha@servidor:porta/banco
    # Usamos "asyncpg" como driver porque nossa API é totalmente assíncrona.
    DATABASE_URL: str

    # ── Clerk (Auth Provider) ─────────────────────────────────────────────────
    # CLERK_JWKS_URL → endpoint público do Clerk com as chaves públicas (JWKS).
    # Usamos essas chaves para verificar a assinatura dos tokens JWT.
    #
    # Formato: https://<seu-app>.clerk.accounts.dev/.well-known/jwks.json
    # Onde encontrar: Clerk Dashboard → API Keys → JWKS URL
    #
    # Por que JWKS e não uma chave estática?
    # O Clerk rotaciona suas chaves periodicamente por segurança.
    # Buscando via URL sempre temos a chave mais recente.
    CLERK_JWKS_URL: str = ""

    # CLERK_AUDIENCE → opcional, para validar o campo "aud" do JWT.
    # Normalmente não é necessário para tokens de sessão do Clerk.
    CLERK_AUDIENCE: str = ""

    # ── Configuração do Pydantic Settings ─────────────────────────────────────
    # env_file=".env" → lê variáveis do arquivo .env na raiz do projeto
    # env_ignore_empty=True → ignora variáveis definidas mas com valor vazio
    # extra="ignore" → ignora variáveis no .env que não estão aqui
    model_config = SettingsConfigDict(
        env_file=".env",
        env_ignore_empty=True,
        extra="ignore",
    )


# ── Instância Singleton ───────────────────────────────────────────────────────
# Criamos uma única instância que é importada pelo resto do projeto.
# Singleton = objeto criado uma vez e reutilizado em toda a aplicação.
settings = Settings()
