from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# 1. O "Engine" (Motor) é o responsável por gerenciar a comunicação real com o banco de dados.
# Ele cria e mantém as conexões nos bastidores usando a URL que configuramos no .env.
# echo=True faz com que todos os comandos SQL gerados sejam impressos no terminal.
# IMPORTANTE: O connect_args={"statement_cache_size": 0} é obrigatório ao usar o Connection Pooler do Supabase.
engine = create_async_engine(
    settings.DATABASE_URL, 
    echo=True,
    connect_args={"statement_cache_size": 0}
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
