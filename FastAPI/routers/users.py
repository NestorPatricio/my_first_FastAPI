"""Aprendiendo a usar FastAPI.
Se genera un CRUD con una lista de instancias de modelo 'User'.

Esta ruta se activa desde main.
"""

from fastapi import APIRouter
from fastapi import HTTPException
from pydantic import BaseModel


# Instancia de la ruta de la API
router = APIRouter(tags=['Users'])


# Modelos de datos de usuarios
class User(BaseModel):
    """Modelo para definir informarción de usuarios, no de la API."""
    id: int
    name: str
    surname: str
    url: str
    age: int


# Datos para ser consultados
users_list: list[User] = [
    User(
        id=1,
        name='Brais',
        surname='Moure',
        url='https://moure.dev',
        age=35
    ),
    User(
        id=2,
        name='Moure',
        surname='Dev',
        url='https://mouredev.com',
        age=36
    ),
    User(
        id=3,
        name='Haakon',
        surname='Dahlberg',
        url='https://haakon.com',
        age=33
    ),
]


# Funciones generales
def search_user(user_id: int):
    """Busca un usario por número de id."""
    users = filter(lambda user: user.id == user_id, users_list)
    try:
        return list(users)[0]
    except IndexError as e:
        raise HTTPException(status_code=404, detail='User id not found') from e

def generate_id_list():
    """Genera una lista con los numeros de id de los usuarios guardados."""
    return [user.id for user in users_list]


# Endpoints de la ruta
@router.get(path='/users-json')
async def users_json():
    """Endopoint para mostrar a todos los usuarios desde un json."""
    return [
        {
            'name': 'Brais',
            'surname' : 'Moure',
            'url': 'https://moure.dev',
            'age': 35,
        },
        {
            'name': 'Moure',
            'surname' : 'Dev',
            'url': 'https://mouredev.com',
            'age': 36,
        },
        {
            'name': 'Haakon',
            'surname' : 'Dahlberg',
            'url': 'https://haakon.com',
            'age': 33,
        },
    ]

@router.get(path='/users-class')
async def users_class():
    """Endopoint para mostrar los usuarios desde instancias de 'User'."""
    return users_list

@router.get(path='/user/{user_id}', response_model=User)
async def user_by_id_path(user_id: int):
    """Endpoint para buscar un usuario por id por path."""
    return search_user(user_id=user_id)

@router.get(path='/user-query', response_model=User)
async def user_by_id_query(user_id: int):
    """Endpoint para buscar un usuario por id por query."""
    return search_user(user_id=user_id)

@router.post(path='/user', response_model=User, status_code=201)
async def add_user(new_user: User):
    """Endpoint para añadir un nuevo usuario."""
    if new_user.id in generate_id_list():
        raise HTTPException(status_code=406, detail='User id already exists')

    users_list.append(new_user)
    return new_user

@router.put(path='/user', response_model=User, status_code=201)
async def update_user_info(updated_user: User):
    """Endpoint para actualizar la información de algún usuario."""
    for index, user in enumerate(users_list):
        if user.id == updated_user.id:
            users_list[index] = updated_user
            return updated_user

    raise HTTPException(status_code=404, detail='User not found')

@router.delete(path='/user{user_id}', status_code=204)
async def delete_user(user_id: int):
    """Endpoint para eliminar un usuario por id."""
    for index, user in enumerate(users_list):
        if user.id == user_id:
            users_list.pop(index)
            return 'User deleted'

    raise HTTPException(status_code=404, detail='User not found')
