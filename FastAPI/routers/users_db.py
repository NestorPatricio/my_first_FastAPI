"""Aprendiendo a usar FastAPI.
Se genera un CRUD con una lista de instancias de modelo 'User'.
La información se obtiene desde una base de datos de MongoDB.

Esta ruta se activa desde main.
"""

from typing import Any

from fastapi import APIRouter
from fastapi import HTTPException
from fastapi import status
from bson import ObjectId

from FastAPI.db.client import database
from FastAPI.db.models.user import User
from FastAPI.db.schemas.user import user_schema
from FastAPI.db.schemas.user import users_schema


# Instancia de la ruta de la API
router = APIRouter(
    prefix='/users-db',
    tags=['Users_in_Atlas'],
    responses={status.HTTP_404_NOT_FOUND: {'message': 'User not found'}}
)


# Datos para ser consultados
users_list: list[User] = [] # Esta variable se ha de eliminar en algún momento


# Funciones generales
def search_user(field: str, value: Any) -> User | None:
    """Busca un usario de la base de datos de MongoDB por un atributo definido y su valor."""
    try:
        user: dict[str, Any] | None = database.users.find_one(
            filter={field: value},
        )
        if user:
            return user_schema(user_from_db=user)

        return None

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User email not found',
        ) from e


# Endpoints de la ruta
@router.get(path='/', response_model=list[User | None])
async def users():
    """Endopoint para mostrar todos los usuarios desde la base de datos de MongoDB."""
    return users_schema(users_from_db=list(database.users.find()))

@router.get(path='/id/{user_id}', response_model=User)
async def user_by_id_path(user_id: str):
    """Endpoint para buscar un usuario desde la base de datos de MongoDB según id, por path."""
    if user := search_user(field='_id', value=ObjectId(user_id)):
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='User email not found',
    )

@router.get(path='/by-query', response_model=User)
async def user_by_id_query(user_id: str):
    """Endpoint para buscar un usuario desde la base de datos de MongoDB según id, por query."""
    if user := search_user(field='_id', value=ObjectId(user_id)):
        return user
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='User id not found',
    )

@router.post(path='/', response_model=User, status_code=status.HTTP_201_CREATED)
async def add_user(new_user: User):
    """Endpoint para añadir un nuevo usuario a la base de datos de MongoDB."""
    if search_user(field='email', value=new_user.email):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail='User id already exists',
        )

    user_dict = dict(new_user)
    del user_dict['id']
    user_id = database.users.insert_one(document=user_dict).inserted_id

    if saved_user := database.users.find_one(filter={'_id': user_id}):
        return user_schema(user_from_db=saved_user)

@router.put(path='/', response_model=User, status_code=status.HTTP_201_CREATED)
async def update_user_info(updated_user: User):
    """Endpoint para actualizar la información de algún usuario de la base de datos de MongoDB."""
    try:
        user_dict: dict[str, Any] = dict(updated_user)
        del user_dict['id']

        database.users.find_one_and_replace(
            filter={'_id': ObjectId(updated_user.id)},
            replacement=user_dict,
        )
        return search_user(field='_id', value=ObjectId(updated_user.id))

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        ) from e

@router.delete(path='/{user_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(user_id: str):
    """Endpoint para eliminar un usuario de la base de datos de MongoDB según id, por path."""
    deleted = database.users.find_one_and_delete(
        filter={'_id': ObjectId(user_id)},
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found',
        )
