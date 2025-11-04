from fastapi import FastAPI
from routers.user import router as users_router
from routers.books import router as books_router
from routers.stats import router as stats_router
from routers.scraping import router as scraping_router
from routers.health import router as health_router
from fastapi.openapi.utils import get_openapi

app = FastAPI(
    title="Tech Challenge 1 - Machine Learning - FIAP",
    version="1.0.0",
    description="""
              ## 🔐 Como fazer login

              1. Vá até a rota `/api_login`.
              2. Envie uma requisição **POST** com o corpo JSON:
              ```json
              {
                "username": "henrique",
                "password": "teste123"
              }
              ```
              3. Você receberá um token JWT como resposta.
              4. Copie esse token e clique no botão "Authorize" no topo da documentação Swagger.
              5. Cole o token no formato: `Bearer <seu_token_aqui>`
              6. Agora você pode acessar as rotas protegidas.
              """
)

# Registrar routers
app.include_router(users_router)
app.include_router(books_router)
app.include_router(stats_router)
app.include_router(scraping_router)
app.include_router(health_router)

# 🔒 Configurar autenticação Bearer no Swagger
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )

    # Define o esquema de segurança
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }

    # Aplica o esquema de segurança globalmente
    for path in openapi_schema["paths"]:
        for method in openapi_schema["paths"][path]:
            openapi_schema["paths"][path][method]["security"] = [{"BearerAuth": []}]

    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi
