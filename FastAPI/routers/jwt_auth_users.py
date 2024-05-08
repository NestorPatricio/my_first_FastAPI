"""Aprendiendo a usar FastAPI.
Página para aprender a gestionar usuarios usando JWT.

Las hash de las conraseñas han sido generados usando el esquema 'Bcrypt', siendo las originales
'12345678', '56781234' y '87654321'.

La llave secreta es un número aleatorio de 32 cifras en hexadecimal.

Se activa desde main.
"""

from datetime import datetime
from datetime import timedelta
from datetime import UTC

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt
from jose import JWTError
from passlib.context import CryptContext
from pydantic import BaseModel


# Constantes
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = 'b10d8cb8c5bafd17f60f5045f0e5197cb9ddc8d1ee0995ab482b92acafb50ec7'


# Instancia de la ruta de la API.
router = APIRouter()


# Instancia del sistema de autenticación.
oauth2 = OAuth2PasswordBearer(tokenUrl='login')


# Contexto de encriptación.
crypt = CryptContext(schemes=['bcrypt'])


# Modelos a usar.
class User(BaseModel):
    """Modelo de usuario de la API."""
    username: str
    full_name: str
    email: str
    disabled: bool


class UserDB(User):
    """Modelo de usuario autenticalbe con contraseña de la API."""
    password: str


# Base de datos de los usuarios.
users_db = {
    'mouredev': {
        'username': 'mouredev',
        'full_name': 'Brais Moure',
        'email': 'braismoure@mouredev.com',
        'disabled': False,
        'password': '$2a$12$qdzw6Sf2FZ9kXS32RAkFA.7gGBqspyBJs2AyXRaCMv4dvFdCIKXZe',
    },
    'nestorprr': {
        'username': 'nestorprr',
        'full_name': 'Néstor Rojas',
        'email': 'nestitor@mouredev.com',
        'disabled': False,
        'password': '$2a$12$ENOEUk1UyAQ6ftlqs2e.W.LspqPmDOPcVRviv58w0OUfTJSGf6GLy',
    },
    'patricionrr': {
        'username': 'patricionrr',
        'full_name': 'Patricio Ríos',
        'email': 'patorios@gmail.com',
        'disabled': True,
        'password': '$2a$12$YirGrtvjpyqeeEz..o2jm.bFmRxSdfblx3t8hGYxNF7LUFh6B0mxS',
    }
}


# Funciones generales.
def search_user(username: str):
    """Busca los datos de un usuario en la base de datos.
    Retorna una instancia de 'User'.
    """
    if username in users_db:
        return User(**users_db[username]) # type: ignore
    return None

def search_user_db(username: str):
    """Busca los datos de un usuario en la base de datos.
    Retorna una instancia de 'UserDB'.
    """
    if username in users_db:
        return UserDB(**users_db[username]) # type: ignore
    return None

async def authenticate_token(token: str = Depends(oauth2)):
    """Autentica el token generado al autenticar el usuario.
    Retorna la información del usuario autenticado como instancia de 'User'.
    """
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail='Invalid authentication credentials',
        headers={'WWW-Authenticate': 'Bearer'},
    )

    try:
        username = jwt.decode(
            token=token,
            key=SECRET,
            algorithms=ALGORITHM,
        ).get('sub')

        if not username:
            raise exception

    except JWTError as e:
        raise exception from e

    return search_user(username)

def current_user(user: User = Depends(authenticate_token)):
    """Retorna la información de un usuario autenticado si es que no está inactivo."""
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Disabled user',
        )
    return user


# Endpoints de la API.
@router.post(path='/login')
async def login(form: OAuth2PasswordRequestForm = Depends()):
    """Endpoint para autenticar el 'username' y la contraseña de un usuario de la API."""
    user_db = search_user_db(form.username)
    if not user_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Username not found'
        )

    if not crypt.verify(secret=form.password, hash=user_db.password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail='Wrong password'
        )

    access_token = {
        "sub": user_db.username,
        "exp": datetime.now(tz=UTC) + timedelta(minutes=ACCESS_TOKEN_DURATION),
    }

    return {
        'access_token': jwt.encode(
            claims=access_token,
            key=SECRET,
            algorithm=ALGORITHM
        ),
        'token_type': 'bearer',
    }

@router.get(path='/users/me')
async def current_user_data(user: User = Depends(current_user)):
    """Endpoint para mostrar los datos del usuario actual de la API."""
    return user
