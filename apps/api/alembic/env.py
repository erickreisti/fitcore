import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context
from app.core.config import settings
from app.core.database import Base
from app.models import *  # Isso carrega as tabelas para o Alembic conseguir ler o Base.metadata completo

# Este é o objeto de Configuração do Alembic, que fornece
# acesso aos valores dentro do arquivo alembic.ini em uso.
config = context.config

# Interpreta o arquivo de configuração para o sistema de logs do Python.
# Esta linha basicamente configura os loggers (mensagens de texto no terminal).
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Adicione o objeto MetaData do seu modelo aqui
# para dar suporte ao 'autogenerate' (geração automática de migrações).
target_metadata = Base.metadata

# Importando a URL do banco do nosso .env em vez de ler do alembic.ini
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Outros valores da configuração podem ser obtidos aqui, se necessário:
# minha_opcao = config.get_main_option("minha_opcao")
# ... etc.


def run_migrations_offline() -> None:
    """Roda as migrações em modo 'offline'.

    Isso configura o contexto com apenas uma URL e não um Engine (Motor).
    Ao pular a criação do Engine, nós nem precisamos que o banco de dados 
    esteja online ou disponível no momento.

    Chamadas para context.execute() aqui irão apenas cuspir as strings SQL 
    na tela em vez de rodá-las de verdade no banco.
    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """Neste cenário (online e assíncrono) nós precisamos criar um Engine
    e associar a conexão ativa com o contexto do Alembic.
    """

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args={"statement_cache_size": 0},
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Roda as migrações em modo 'online' (conectado de verdade ao banco)."""

    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
