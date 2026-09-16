from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# 1. O "Engine" (Motor) é o responsável por gerenciar a comunicação real com o banco.
# Ele cria e mantém as conexões nos bastidores usando a URL configurada no .env.
#
# Sobre o nosso banco:
#   → Banco de dados: Neon (PostgreSQL Serverless)
#   → Auth provider: Clerk (separado — só cuida de login/tokens JWT)
#
# echo=True → imprime todos os comandos SQL no terminal (útil em desenvolvimento,
#             desativar em produção para não logar dados sensíveis).
#
# connect_args={"statement_cache_size": 0}
#   → OBRIGATÓRIO quando usamos connection pooling (como o do Neon via PgBouncer).
#   → Sem isso, queries falhariam com erros crypticos usando asyncpg.
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True,
    connect_args={"statement_cache_size": 0},
)

# 2. O "SessionLocal" é uma "fábrica" de sessões.
# Uma Sessão (Session) é como se fosse uma "conversa" temporária com o banco.
# Toda vez que formos salvar um aluno ou buscar um plano, abriremos uma "sessão", faremos a operação e fecharemos.
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# 3. O "Base" é a classe mãe de todos os nossos modelos (tabelas).
# Quando criarmos a tabela de Alunos no código Python, a classe Aluno vai herdar de `Base`.
# Isso diz ao SQLAlchemy: "Olhe para todas as classes que herdam de Base e as transforme em tabelas reais".
Base = declarative_base()

# 4. Esta é uma função auxiliadora (uma "dependência" no FastAPI).
# Ela garante que a API vai abrir a conexão com o banco quando uma requisição começar,
# e VAMOS FECHAR a conexão de forma segura quando a requisição terminar.
async def get_db():
    async with SessionLocal() as session:
        yield session
