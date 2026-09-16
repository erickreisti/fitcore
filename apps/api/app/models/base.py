from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


# ─── TimestampMixin ──────────────────────────────────────────────────────────
#
# Um "Mixin" é uma classe auxiliar que não representa uma tabela sozinha,
# mas adiciona colunas/comportamentos reutilizáveis a outros models.
#
# Por que usar isso?
# Todos os nossos models (Organization, Unit, User, Plan, etc.) precisam
# saber QUANDO foram criados e QUANDO foram atualizados pela última vez.
# Em vez de repetir as mesmas duas colunas em cada arquivo (violando o
# princípio DRY — Don't Repeat Yourself), centralizamos aqui.
#
# Como usar:
#   class MinhaTabela(TimestampMixin, Base):
#       __tablename__ = "minha_tabela"
#       ...
#
# O Python herda da esquerda para a direita. O MRO (Method Resolution Order)
# garante que as colunas do Mixin sejam incluídas na tabela corretamente.
#
# IMPORTANTE — SQLAlchemy 2.x:
# No estilo moderno "Annotated Declarative", as colunas de um Mixin DEVEM
# usar Mapped[tipo] nas type annotations. Sem isso, o SQLAlchemy não consegue
# interpretar corretamente se a anotação é uma coluna mapeada ou outra coisa.
# ─────────────────────────────────────────────────────────────────────────────

class TimestampMixin:
    """Adiciona as colunas created_at e updated_at a qualquer model."""

    # Mapped[datetime] → diz ao SQLAlchemy: "este atributo é uma coluna
    # mapeada do tipo datetime". É o contrato do estilo moderno do ORM.
    #
    # server_default=func.now() → o BANCO DE DADOS preenche este campo
    # automaticamente no momento do INSERT com a hora atual do servidor.
    # Usar server_default (no banco) é mais seguro do que default (no Python),
    # pois garante consistência mesmo se alguém inserir diretamente via SQL.
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    # Mapped[datetime | None] → permite que o valor seja None (NULL no banco).
    # updated_at começa como NULL e só recebe valor no primeiro UPDATE.
    # onupdate=func.now() → o SQLAlchemy atualiza este campo automaticamente
    # toda vez que o registro for modificado via ORM.
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        onupdate=func.now(),
        nullable=True,
    )
