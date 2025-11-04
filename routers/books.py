from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import Optional
from database import get_session
from crud import books as crud_books

router = APIRouter(prefix="/api/v1/books", tags=["Books"])


@router.get("/")
def get_books(session: Session = Depends(get_session)):
    result = crud_books.get_all_books(session)
    return [book.__dict__ for book in result]

@router.get("/search")
def search_books(
    title: Optional[str] = Query(None),
    category: Optional[str] = Query(None),
    session: Session = Depends(get_session)
):
    result = crud_books.search_books(session, title, category)
    if not result:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado")
    return [book.__dict__ for book in result]

@router.get("/top-rated")
def top_rated_books(limit: int = 10, session: Session = Depends(get_session)):
    result = crud_books.get_top_rated_books(session, limit)
    if not result:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado")
    return [book.__dict__ for book in result]

@router.get("/price-range")
def books_by_price_range(
    min: float = Query(...), max: float = Query(...),
    session: Session = Depends(get_session)
):
    if min > max:
        raise HTTPException(status_code=400, detail="Preço mínimo não pode ser maior que o máximo")
    result = crud_books.get_books_by_price_range(session, min, max)
    if not result:
        raise HTTPException(status_code=404, detail="Nenhum livro encontrado nessa faixa de preço")
    return [book.__dict__ for book in result]

@router.get("/categories")
def categories(session: Session = Depends(get_session)):
    return crud_books.list_categories(session)


@router.get("/{book_id}")
def book_by_id(book_id: int, session: Session = Depends(get_session)):
    book = crud_books.get_book_by_id(session, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Livro não encontrado")
    return book.__dict__


