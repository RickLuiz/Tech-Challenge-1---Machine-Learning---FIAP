from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_session
from crud import books as crud_books

router = APIRouter(tags=["Health"])

@router.get("/api/v1/health")
def health_check(session: Session = Depends(get_session)):
    """
    Rota de health check da API.
    Verifica conexão com o banco de dados e retorna total de livros.
    """
    try:
        total_livros = crud_books.get_total_books(session)
        return {
            "status": "ok",
            "database_connected": True,
            "total_books": total_livros
        }
    except Exception as e:
        return {
            "status": "error",
            "database_connected": False,
            "error": str(e)
        }
