from sqlalchemy.orm import Session
from sqlalchemy import and_, func, distinct
from models import Book
from sqlalchemy.orm import Session
from models import Book

def get_all_books(session: Session):
    return session.query(Book).all()

def search_books(session: Session, title: str = None, category: str = None):
    filters = []
    if title:
        filters.append(Book.titulo.ilike(f"%{title}%"))
    if category:
        filters.append(Book.categoria.ilike(f"%{category}%"))
    if not filters:
        return None
    return session.query(Book).filter(and_(*filters)).all()

def get_book_by_id(session: Session, book_id: int):
    return session.query(Book).filter(Book.id == book_id).first()

def get_top_rated_books(session: Session, limit: int = 10):
    return session.query(Book).order_by(Book.rating.desc()).limit(limit).all()

def list_categories(session: Session):
    results = session.query(distinct(Book.categoria)).all()
    return [c[0] for c in results if c[0] is not None]

def get_books_by_price_range(session: Session, min_price: float, max_price: float):
    return session.query(Book).filter(Book.preco >= min_price, Book.preco <= max_price).all()



def get_total_books(session: Session) -> int:
    """
    Retorna a contagem total de livros no banco.
    """
    return session.query(Book).count()

