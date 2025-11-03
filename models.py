from sqlalchemy import Column, Integer, Float, String
from sqlalchemy.ext.declarative import declarative_base

# Base para todos os modelos
Base = declarative_base()

class Book(Base):
    __tablename__ = "books"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    titulo = Column(String, nullable=False)
    preco = Column(Float, nullable=False)
    rating = Column(Integer, nullable=False)
    disponibilidade = Column(String)
    categoria = Column(String)
    imagem = Column(String)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
