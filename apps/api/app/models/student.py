from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

# Ao herdar de 'Base', o SQLAlchemy entende que esta classe será uma tabela no banco.
class Student(Base):
    # __tablename__ define o nome exato da tabela lá no PostgreSQL.
    # É uma boa prática usar nomes no plural e em minúsculo.
    __tablename__ = "students"

    # Definindo as colunas da nossa tabela:
    # primary_key=True diz que este é o identificador único de cada aluno.
    # index=True faz com que buscas por ID sejam muito mais rápidas.
    id = Column(Integer, primary_key=True, index=True)
    
    # nullable=False significa que o nome é OBRIGATÓRIO (não pode ser nulo).
    name = Column(String, nullable=False)
    
    # unique=True garante que não existirão dois alunos com o mesmo email.
    email = Column(String, unique=True, index=True, nullable=False)
    
    phone = Column(String, nullable=True) # Telefone é opcional
    
    # O padrão (default) será True. Todo aluno cadastrado nasce "ativo".
    is_active = Column(Boolean, default=True)
    
    # server_default=func.now() preenche automaticamente a data de criação com a hora do servidor.
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # onupdate=func.now() atualiza este campo automaticamente toda vez que editarmos o aluno.
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
