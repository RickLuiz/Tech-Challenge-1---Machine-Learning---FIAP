📚 Tech Challenge 1 - FIAP
🔹 Descrição do Projeto

Trata-se de uma API desenvolvida em FastAPI que permite gerenciar uma coleção de livros, realizando operações de consulta, busca, scraping de dados e análise de estatísticas.

O projeto tem como objetivos principais:

Criar e consultar usuários com autenticação JWT.

Armazenar e consultar informações de livros em banco de dados SQLite (ou outro banco relacional).

Realizar scraping de livros de sites públicos e armazenar os dados.

Disponibilizar endpoints para estatísticas de livros, categorias, preço, rating e mais.

Fornecer um endpoint de health check para monitoramento da API.

🔹 Tecnologias Utilizadas

Python 3.11+

FastAPI – framework web para APIs

SQLAlchemy – ORM para banco de dados

SQLite – banco de dados local (pode ser substituído por MySQL/PostgreSQL)

Passlib + bcrypt – hash seguro de senhas

JWT (PyJWT) – autenticação baseada em tokens

BeautifulSoup + Requests – scraping de dados de livros

Pandas – manipulação e exportação de dados

🔹 Como Rodar o Projeto Localmente

1 - Clone o repositório:

git clone https://github.com/RickLuiz/Tech-Challenge-1---Machine-Learning---FIAP/tree/main
cd TECH CHALLENGE 1 

2 - Crie um ambiente virtual:

python -m venv venv
source venv/bin/activate  # Linux / Mac
venv\Scripts\activate     # Windows

3 - Instale as dependências:

pip install -r requirements.txt

4 - Crie o arquivo .env na raiz do projeto com a seguinte variável:

JWT_SECRET_KEY=SUA_CHAVE_SECRETA

5 - Rode a API:

uvicorn main:app --reload

6 - Acesse a documentação interativa em:

http://127.0.0.1:8000/docs
ou
http://127.0.0.1:8000/redoc


🔹 Endpoints da API

Usuários
| Endpoint               | Método | Descrição                         |
| ---------------------- | ------ | --------------------------------- |
| `/api/v1/register`     | POST   | Cria um novo usuário              |
| `/api/v1/login`        | POST   | Realiza login e retorna token JWT |
| `/api/v1/auth/refresh` | POST   | Renova token JWT                  |


Livros
| Endpoint                    | Método | Descrição                                   |
| --------------------------- | ------ | ------------------------------------------- |
| `/api/v1/books/`            | GET    | Lista todos os livros                       |
| `/api/v1/books/search`      | GET    | Busca livros por título ou categoria        |
| `/api/v1/books/top-rated`   | GET    | Retorna livros com maior rating             |
| `/api/v1/books/price-range` | GET    | Retorna livros dentro de uma faixa de preço |
| `/api/v1/books/categories`  | GET    | Lista todas as categorias de livros         |
| `/api/v1/books/{book_id}`   | GET    | Retorna informações de um livro específico  |


Scraping
| Endpoint                   | Método | Descrição                               |
| -------------------------- | ------ | --------------------------------------- |
| `/api/v1/scraping/trigger` | GET    | Inicia scraping de livros em background |


Estatísticas
| Endpoint                   | Método | Descrição                             |
| -------------------------- | ------ | ------------------------------------- |
| `/api/v1/stats/overview`   | GET    | Estatísticas gerais da coleção        |
| `/api/v1/stats/categories` | GET    | Estatísticas detalhadas por categoria |

Health Check
| Endpoint         | Método | Descrição                                          |
| ---------------- | ------ | -------------------------------------------------- |
| `/api/v1/health` | GET    | Verifica status da API e conectividade com o banco |

🔹 Links

Repositório GitHub: https://github.com/RickLuiz/Tech-Challenge-1---Machine-Learning---FIAP/tree/main

Deploy da API: https://tech-challenge-1-machine-learning-f.vercel.app/docs

Vídeo demonstrativo: https://youtu.be/yhd9wLAAJhg


Credênciais de login em produção:
Na Vercel tem um usuário teste que pode ser acessado com as credênciais:

username:"henrique"
password:'teste123

🔹 Arquitetura do Projeto:

(https://github.com/RickLuiz/Tech-Challenge-1---Machine-Learning---FIAP/blob/main/Tech%20Challenge%201.drawio.png?raw=true)


🔹 Observações

Senhas são armazenadas de forma segura com hash bcrypt.

Token JWT possui expiração configurável via .env.

Scraping é executado em background, permitindo que a API continue respondendo a outras requisições.

Arquivo CSV dos livros é gerado automaticamente após o scraping.