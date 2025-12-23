from sqlalchemy import create_engine, Column, Integer, String, Date, ForeignKey, Boolean,LargeBinary
from sqlalchemy.dialects.mysql import MEDIUMTEXT
from sqlalchemy.orm import declarative_base, relationship
from datetime import date

db = create_engine(
    'mysql+mysqlconnector://root:123456789@localhost:3306/ecoplay'
)

Base = declarative_base()

#Classe para criacao de usuario

class Usuario(Base):
    __tablename__ = 'usuarios'
    
    id = Column(Integer, primary_key=True)
    # equipe_id = Column(Integer, ForeignKey('equipes.id'))
    nome_completo = Column(String(255), nullable=False)
    sexo = Column(String(1), nullable=False)  # 'M' ou 'F'
    data_nascimento = Column(Date, nullable=False)
    funcao = Column(String(50), nullable=False)  # Atuante, Líder, Vice, Fiscal, Suplente
    telefone_pessoal = Column(String(20), nullable=False)
    rg_path = Column(LargeBinary)
    cpf_path = Column(LargeBinary)
    email = Column(String(100), nullable=False)
    senha_hash = Column(String(255), nullable=True)
    cursando = Column(String(50), nullable=False)  # Fundamental 1, Fundamental 2, Universitário
    manequim = Column(String(10), nullable=False)  # PP, P, M, G, GG
    tipo_sanguineo = Column(String(5), nullable=False)  # A+, O-, etc.
    medicamento_controlado = Column(Boolean, nullable=False, default=False)
    nome_medicamento_1 = Column(String(100), nullable=True)
    declaracao_lida = Column(Boolean, nullable=False, default=False)
    
    # Relacionamento com a tabela Equipe (comentado para testes)
    # equipe = relationship("Equipe", back_populates="usuarios")
    
   
    
    def __init__(self, nome_completo, sexo, data_nascimento, funcao, telefone_pessoal, 
                 rg_path, cpf_path, email, senha_hash=None, cursando=None, manequim=None, tipo_sanguineo=None, 
                 medicamento_controlado=False, nome_medicamento_1=None, 
                 declaracao_lida=False):  # equipe_id removido para testes
        """
        Construtor da classe Usuario
        """

        self.nome_completo = nome_completo
        self.sexo = sexo
        self.data_nascimento = data_nascimento
        self.funcao = funcao
        self.telefone_pessoal = telefone_pessoal
        self.rg_path = rg_path
        self.cpf_path = cpf_path
        self.email = email
        self.senha_hash = senha_hash
        self.cursando = cursando
        self.manequim = manequim
        self.tipo_sanguineo = tipo_sanguineo
        self.medicamento_controlado = medicamento_controlado
        self.nome_medicamento_1 = nome_medicamento_1
        self.declaracao_lida = declaracao_lida
        # self.equipe_id = equipe_id  # Comentado para testes sem equipe id
    
    def __repr__(self):
        return f"<Usuario(id={self.id}, nome='{self.nome_completo}')>"




#Classe para criacao de equipe
class Equipe(Base):
    __tablename__ = 'equipes'
    
    id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=True)  # Opcional
    aceito = Column(Boolean, nullable=False, default=False)
    total_components = Column(Integer, nullable=False, default=0)
    
    # Relacionamento com a tabela Usuario (comentado para testes)
    # usuarios = relationship("Usuario", back_populates="equipe", cascade="all, delete-orphan")

    
    def __init__(self, nome=None, aceito=False, total_components=0):
        """
        Construtor da classe Equipe
        
        """
        self.nome = nome
        self.aceito = aceito
        self.total_components = total_components
    
    def __repr__(self):
        return f"<Equipe(id={self.id}, nome='{self.nome}', aceito={self.aceito})>"




Base.metadata.create_all(db)