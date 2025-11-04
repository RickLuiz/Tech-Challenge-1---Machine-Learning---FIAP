from fastapi import FastAPI
from routers.user import router as users_router
from routers.books import router as books_router
from routers.stats import router as stats_router
from routers.scraping import router as scraping_router
from routers.health import router as health_router



app = FastAPI(title="Tech Challenge 1 - Machine Learning - FIAP", version="1.0.0", description="""
              ## 🔐 Como fazer login

                    1. Vá até a rota `/api_login`.
                    2. Envie uma requisição **POST** com o corpo JSON:
                    ```json
                    {
                    "username": "henrique",
                    "password": "teste123"
                    }

                    3. Você receberá um token JWT como resposta.

                    4. Copie esse token e clique no botão "Authorize" no topo da documentação Swagger.

                    5. Cole o token no formato: Bearer 

                    6. Agora você pode acessar as rotas protegidas.
              
              """)

# Registrar routers
app.include_router(users_router)
app.include_router(books_router)
app.include_router(stats_router)
app.include_router(scraping_router)
app.include_router(health_router)

