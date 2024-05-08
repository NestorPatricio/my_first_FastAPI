"""Aprendiendo a usar FastAPI.
Modelo de usuario para ser usado con la información de la base de datos de MongoDB.
"""

from pydantic import BaseModel


class User(BaseModel):
    """Modelo para definir informarción de usuarios, no de la API."""
    id: str | None = None
    username: str
    email: str
