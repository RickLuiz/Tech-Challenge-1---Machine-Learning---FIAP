from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_session
from models import Book

router = APIRouter(prefix="/api/v1/stats", tags=["Stats"])

@router.get("/overview")
def stats_overview(session: Session = Depends(get_session)):
    total_books = session.query(func.count(Book.id)).scalar()
    avg_price = session.query(func.avg(Book.preco)).scalar() or 0
    avg_price = round(avg_price, 2)

    dist = {
        "excelente (>=4.8)": session.query(func.count(Book.id)).filter(Book.rating >= 4.8).scalar(),
        "bom (4.5–4.79)": session.query(func.count(Book.id)).filter(Book.rating.between(4.5, 4.79)).scalar(),
        "regular (<4.5)": session.query(func.count(Book.id)).filter(Book.rating < 4.5).scalar()
    }

    return {
        "total_books": total_books,
        "average_price": avg_price,
        "rating_distribution": dist
    }

@router.get("/categories")
def stats_by_category(session: Session = Depends(get_session)):
    results = session.query(
        Book.categoria.label("categoria"),
        func.count(Book.id).label("total_livros"),
        func.avg(Book.preco).label("preco_medio"),
        func.min(Book.preco).label("preco_minimo"),
        func.max(Book.preco).label("preco_maximo")
    ).group_by(Book.categoria).order_by(Book.categoria).all()

    stats = []
    for row in results:
        stats.append({
            "categoria": row.categoria,
            "total_livros": row.total_livros,
            "preco_medio": round(row.preco_medio or 0, 2),
            "preco_minimo": round(row.preco_minimo or 0, 2),
            "preco_maximo": round(row.preco_maximo or 0, 2)
        })

    return {"categorias": stats}
