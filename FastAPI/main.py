"""Aprendiendo a usar FastAPI.

Para activar la API: $uvicorn main:app --reload
Dirección IP de la API: http://127.0.0.1/

Documentación de API proveída por Swagger UI: http://127.0.0.1/docs
Documentación de API proveída por ReDoc: http://127.0.0.1/redoc
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from FastAPI.routers import jwt_auth_users
from FastAPI.routers import products
from FastAPI.routers import users
from FastAPI.routers import users_db


# Instancia de la app de FastAPI.
app = FastAPI(
    title="Conociendo FastAPI",
    version="0.0.1",
    description="API creada para aprender a usar FastAPI y el protocolo REST",
)


# Routers de las API.
app.include_router(router=jwt_auth_users.router)
app.include_router(router=products.router)
app.include_router(router=users.router)
app.include_router(router=users_db.router)


# Montando recursos estáticos.
app.mount(path='/static', app=StaticFiles(directory='FastAPI/static'))


# Endpoints de la API base.
@app.get(path='/')
async def root():
    """Endpoint de bienvenida de la app."""
    return '¡Hola, hola, Coca-Cola, FastAPI!'

@app.get(path='/url')
async def url():
    """Endpoint de prueba para devolver un pequeño JSON."""
    return {'url': 'https://mouredev.com/python'}
