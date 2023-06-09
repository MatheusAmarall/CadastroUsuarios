from infra.configs.base import Base
from sqlalchemy import Column, String, Integer

class Cliente(Base):
    __tablename__ = 'cliente'

    cpf = Column(String(100), unique=True, primary_key=True)
    nome = Column(String(100), nullable=False)
    telefone_fixo = Column(String(100), nullable=False)
    telefone_celular = Column(String(100), nullable=False)
    sexo = Column(String(100), nullable=False)
    cep = Column(String(100), nullable=False)
    logradouro = Column(String(100), nullable=False)
    numero = Column(String(100), nullable=False)
    complemento = Column(String(100), nullable=False)
    bairro = Column(String(100), nullable=False)
    municipio = Column(String(100), nullable=False)
    estado = Column(String(100), nullable=False)
    