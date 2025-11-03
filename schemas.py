# schemas.py
from pydantic import BaseModel
from typing import Optional

# ----------------------
# Schemas para livros
# ----------------------
class BookModel(BaseModel):
    titulo: str
    preco: float
    rating: int
    disponibilidade: str
    categoria: str
    imagem: str

# ----------------------
# Schemas para usuários
# ----------------------
class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str
