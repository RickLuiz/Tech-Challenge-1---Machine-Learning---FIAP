from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import sessionmaker
from models import Base, Book
from schemas import BookModel
from database import engine, get_session
import requests
from bs4 import BeautifulSoup
import pandas as pd
from auth import get_current_user  

router = APIRouter(prefix="/api/v1/scraping", tags=["Scraping"])


Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def rating_to_int(rating_str):
    ratings = {"One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}
    return ratings.get(rating_str, 0)

def scrape_books():
    session = Session()
    base_url = "https://books.toscrape.com/catalogue/page-{}.html"
    site_base = "https://books.toscrape.com/"
    pagina = 1
    total_inseridos = 0

    try:
        while True:
            url = base_url.format(pagina)
            resposta = requests.get(url)
            resposta.encoding = 'utf-8'
            if resposta.status_code != 200:
                break

            soup = BeautifulSoup(resposta.text, "html.parser")
            artigos = soup.find_all("article", class_="product_pod")
            if not artigos:
                break

            for artigo in artigos:
                try:
                    titulo = artigo.h3.a["title"]
                    preco = float(artigo.find("p", class_="price_color").text.strip()[1:])
                    rating_class = artigo.find("p", class_="star-rating")["class"][1]
                    rating = rating_to_int(rating_class)
                    disponibilidade = artigo.find("p", class_="instock availability").text.strip()
                    img_relativa = artigo.find("img")["src"]
                    img_url = site_base + img_relativa.replace("../../", "")

                    link_relativo = artigo.h3.a["href"]
                    link_completo = site_base + "catalogue/" + link_relativo.replace("../", "")
                    livro_resposta = requests.get(link_completo)
                    livro_resposta.encoding = 'utf-8'
                    livro_soup = BeautifulSoup(livro_resposta.text, "html.parser")
                    categoria = livro_soup.find("ul", class_="breadcrumb").find_all("li")[2].a.text.strip()

                    livro_valido = BookModel(
                        titulo=titulo,
                        preco=preco,
                        rating=rating,
                        disponibilidade=disponibilidade,
                        categoria=categoria,
                        imagem=img_url
                    )

                    book = Book(
                        titulo=livro_valido.titulo,
                        preco=livro_valido.preco,
                        rating=livro_valido.rating,
                        disponibilidade=livro_valido.disponibilidade,
                        categoria=livro_valido.categoria,
                        imagem=livro_valido.imagem
                    )
                    session.add(book)
                    total_inseridos += 1
                except Exception as e:
                    print(f"Livro inválido ignorado: {titulo} | Erro: {e}")

            session.commit()
            pagina += 1

        # Gerar CSV
        conn = engine.raw_connection()
        df = pd.read_sql_query("SELECT * FROM books", conn)
        df.to_csv("books.csv", index=False, encoding="utf-8-sig")
        conn.close()
        print(f"Scraping finalizado! Total de livros inseridos: {total_inseridos}")
    finally:
        session.close()


@router.get("/trigger")
def trigger_scraping(background_tasks: BackgroundTasks, user_id: str = Depends(get_current_user)):
    background_tasks.add_task(scrape_books)
    return {
        "status": "ok",
        "mensagem": "Scraping iniciado em background. Pode levar alguns minutos para completar."
    }
