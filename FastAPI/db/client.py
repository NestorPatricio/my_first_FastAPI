"""Aprendiendo a usar FastAPI.
Página para conectar la API a una base de datos de MongoDB.
"""

from typing import Any

from pymongo.database import Database
from pymongo.mongo_client import MongoClient

from FastAPI.config import get_settings


# La URI para conectarse a la base de datos de Atlas.
URI: str = f'mongodb+srv://{ get_settings().db_user}:{get_settings().db_password}@pruebas.rvm0cpk' \
    '.mongodb.net/?retryWrites=true&w=majority&appName=Pruebas'

# Se instancia una instancia de cliente de MongoDB, indicando la base de datos a usar.
client: MongoClient[dict[str, Any]] = MongoClient(host=URI)
database: Database[dict[str, Any]] = client.pruebas
