import pandas as pd
from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DECIMAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship

# Conexão com o banco de dados MySQL
engine = create_engine('mysql+mysqlconnector://root:senai%40134@127.0.0.1:3306/BD_Clima_Saude', echo=True)

# Base para as classes ORM
Base = declarative_base()

# Tabela 'Pais'
class Pais(Base):
    __tablename__ = 'pais'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    nome = Column(String(100))
    sigla = Column(String(5))
    densidade = Column(Integer)
    area = Column(Float)

# Tabela 'Mortes'
class Mortes(Base):
    __tablename__ = 'mortes'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    id_pais = Column(Integer, ForeignKey('pais.id'))
    ano = Column(Integer)
    quantidade = Column(Integer)

    pais = relationship('Pais')

# Tabela 'Emissao'
class Emissao(Base):
    __tablename__ = 'emissao'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    id_pais = Column(Integer, ForeignKey('pais.id'))
    ano = Column(Integer)
    total = Column(Float)
    carvao = Column(Float)
    petroleo = Column(Float)
    gas = Column(Float)
    cimento = Column(Float)
    queima = Column(Float)
    outros = Column(Float)

    pais = relationship('Pais')

# Tabela 'Temperatura'
class Temperatura(Base):
    __tablename__ = 'temperatura'

    id = Column(Integer, primary_key=True, autoincrement=True, unique=True)
    id_pais = Column(Integer, ForeignKey('pais.id'))
    ano = Column(Integer)
    indice = Column(DECIMAL(10, 2))

    pais = relationship('Pais')

# Criar uma sessão
Session = sessionmaker(bind=engine)
session = Session()

def busca_ou_cria_pais(session, nome, sigla, densidade, area):
    # Verifica se o país já existe. Caso não, cria um novo.
    pais = session.query(Pais).filter_by(nome=nome).first()
    if not pais:
        pais = Pais(nome=nome, sigla=sigla, densidade=densidade, area=area)
        session.add(pais)
        session.commit()
    return pais.id

def inserir_dados(session):
    # Carregando datasets
    df_paises = pd.read_csv('world_data.csv')
    df_mortes = pd.read_csv('cause_of_deaths.csv')
    df_emissao = pd.read_csv('emission_per_country.csv')
    df_temperatura = pd.read_csv('annual_surface_temp.csv')

    # Inserir dados de países
    for _, row in df_paises.iterrows():
        sigla = row['Abbreviation']
        densidade = row['Density(PerKm2)']
        area = row['Land Area(Km2)']

        if(pd.isnull(sigla)):
            sigla = ""

        if(pd.isna(area)):
            area = 0

        if(pd.isna(densidade)):
            densidade = 0

        if(type(area) is str):
            area = row['Land Area(Km2)'].replace(",", "")

        if(type(densidade) is str):
            area = row['Density(PerKm2)'].replace(",", "")

        busca_ou_cria_pais(session, row['Country'], sigla, densidade.replace(",", ""), area)

    # Inserir dados de temperatura
    for _, row in df_temperatura.iterrows():
        id_pais = busca_ou_cria_pais(session, row['Country'], '', None, None)
        temperatura = Temperatura(
            id_pais=id_pais, 
            ano=row['Year'].replace("F", ""), 
            indice=row['Temperature'])
        session.add(temperatura)

    # Inserir dados de emissões
    for _, row in df_emissao.iterrows():

        total=row['Total']
        carvao=row['Coal']
        petroleo=row['Oil']
        gas=row['Gas'] 
        cimento=row['Cement']
        queima=row['Flaring'] 
        outros=row['Other']

        if(pd.isna(total)):
            total = 0

        if(pd.isna(carvao)):
            carvao = 0

        if(pd.isna(petroleo)):
            petroleo = 0

        if(pd.isna(gas)):
            gas = 0

        if(pd.isna(cimento)):
            cimento = 0

        if(pd.isna(queima)):
            queima = 0

        if(pd.isna(outros)):
            outros = 0

        id_pais = busca_ou_cria_pais(session, row['Country'], '', None, None)
        emissao = Emissao(
            id_pais=id_pais, 
            ano=row['Year'], 
            total=total, 
            carvao=carvao,
            petroleo=petroleo, 
            gas=gas, 
            cimento=cimento,
            queima=queima, 
            outros=outros
        )
        session.add(emissao)

    # Inserir dados de mortes
    for _, row in df_mortes.iterrows():

        id_pais = busca_ou_cria_pais(session, row['Country'], '', 0, 0
                                     )
        morte = Mortes(id_pais=id_pais, ano=row['Year'], quantidade=row['Cardiovascular Diseases'])
        session.add(morte)

    session.commit()
    print("Dados inseridos com sucesso!")

if __name__ == "__main__":
    inserir_dados(session)