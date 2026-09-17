# ─────────────────────────────────────────────────────────────────────────────
# PACOTE: app.models
#
# O que é este arquivo?
# O __init__.py transforma a pasta "models" em um pacote Python importável.
#
# Por que importamos os models aqui?
# O Alembic precisa "enxergar" todos os models para gerar as migrations
# automaticamente com --autogenerate. Ele faz isso lendo o objeto Base.metadata,
# que só conhece um model se ele tiver sido importado antes.
#
# ORDEM DE IMPORTAÇÃO IMPORTA:
# Models com Foreign Keys devem ser importados DEPOIS dos models que referenciam.
# Exemplo:
#   → Organization não depende de ninguém       → importa primeiro
#   → Unit depende de Organization               → importa depois
#   → Student depende de Organization e Unit     → importa por último (futuramente)
# ─────────────────────────────────────────────────────────────────────────────

from app.core.database import Base

# Tabelas raiz (sem dependências)
from app.models.organization import Organization

# Tabelas que dependem de Organization
from app.models.unit import Unit

# Usuários do sistema (dependem de Organization e Unit)
from app.models.user import User, UserRole

# Tabelas de alunos (dependem de Organization e Unit)
from app.models.student import Student, StudentStatus, Gender
from app.models.plan import Plan
from app.models.membership import Membership, MembershipStatus

# Opcional, mas útil para exportar tudo quando alguém fizer:
# from app.models import Base, User, Organization...
__all__ = [
    "Base",
    "User",
    "UserRole",
    "Organization",
    "Unit",
    "Student",
    "StudentStatus",
    "Gender",
    "Plan",
    "Membership",
    "MembershipStatus",
]

# Quando criarmos os demais models (User, Plan, Membership, Payment, Attendance),
# adicionaremos os imports aqui na ordem correta.
