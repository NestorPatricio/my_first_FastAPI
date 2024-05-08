"""Aprendiendo a usar FastAPI.
En este archivo se ejecutan las operaciones entre el modelo 'User' y la correspondiente información
proveniente de la base de datos de MongoDB.
"""

from bson import ObjectId

from FastAPI.db.models.user import User


def user_schema(user_from_db: dict[str, str | ObjectId]) -> User:
    """Transforma la información de un usario provenientes de la base de datos de MongoDB,
    retornándola como un objeto 'User'.
    """
    return User(
        **{
            'id': str(user_from_db["_id"]),
            'username': str(user_from_db['username']),
            'email': str(user_from_db['email']),
        },
    )

def users_schema(users_from_db: list[dict[str, str | ObjectId]]) -> list[User]:
    """Transforma la información de varios usarios provenientes de la base de datos de MongoDB,
    retornándola como una lista de objetos 'User'.
    """
    return list(map(user_schema, users_from_db))
