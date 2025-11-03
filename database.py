# database.py
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, declarative_base

# Carrega variáveis do .env
load_dotenv()

# URL do banco (padrão SQLite local)
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///books.db")

# --- Engine SQLAlchemy ---
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

# --- Sessionmaker ---
SessionLocal = sessionmaker(bind=engine, autocommit=False, autoflush=False)

# --- Base declarativa ---
Base = declarative_base()
metadata = MetaData()

# --- Dependency para FastAPI ---
def get_session():
    """
    Fornece uma sessão do SQLAlchemy para ser usada em routes via Depends.
    Exemplo:
        def route(session: Session = Depends(get_session)):
            ...
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
