"""Aprendiendo a usar FastAPI.
Página para aprender a gestionar usuarios de la API.
La información que usa es básica y sencilla, todo con fines didácticos.

Se puede configurar para ser una ruta activada desde main o para activarla desde acá:
$uvicorn basic_auth_user:router --reload
"""

from fastapi import FastAPI
#from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel


# Instancia de la ruta de la API.
#router = APIRouter(prefix='/', tags=['User Manage'])
router = FastAPI()


# Instancia del sistema de autenticación.
oauth2 = OAuth2PasswordBearer(tokenUrl='login')


# Modelo de usuarios de la API.
class User(BaseModel):
    """Modelo de usuario de la API."""
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    """Modelo de usuario autenticable con contraseña de la API."""
    password: str


# Base de datos de los usuarios.
users_db = {
    'mouredev': {
        'username': 'mouredev',
        'full_name': 'Brais Moure',
        'email': 'braismoure@mouredev.com',
        'disabled': False,
        'password': '12345678',
    },
    'nestorprr': {
        'username': 'nestorprr',
        'full_name': 'Néstor Rojas',
        'email': 'nestitor@mouredev.com',
        'disabled': False,
        'password': '56781234',
    },
    'patricionrr': {
        'username': 'patricionrr',
        'full_name': 'Patricio Ríos',
        'email': 'patorios@gmail.com',
        'disabled': True,
        'password': '87654321',
    }
}


# Funciones generales.
def search_user_db(username: str):
    """Busca una instancia de 'UserDB' por su 'username'."""
    if username in users_db:
        return UserDB(**users_db[username]) # type: ignore
    return None

def search_user(username: str):
    """Busca una instancia de 'User' por su 'username'."""
    if username in users_db:
        return User(**users_db[username]) # type: ignore
    return None

async def current_user(token: str = Depends(oauth2)):
    """Devuelve los datos del usuario de la API, en caso de estar activo."""
    user = search_user(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid authentication credentials',
            headers={'WWW-Authenticate': 'Bearer'},
        )

    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Disabled user',
        )
    return user


# Endpoints para autenticación.
@router.post(path='/login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    """Endpoint para autenticar el 'username' y la contraseña de un usuario de la API."""
    user_from_db = users_db.get(form.username)
    if not user_from_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Username not found',
        )

    api_user = search_user_db(form.username)
    if api_user and not api_user.password == form.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Wrong password',
        )

    return {'access_token': api_user.username, 'token_type': 'bearer'}

@router.get(path='/users/me')
async def me(user: User = Depends(current_user)):
    """Endpoint para mostrar los datos del usuario actual de la API."""
    return user
