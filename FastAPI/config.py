"""Aprendiendo a usar FastAPI.
Archivo de configuración para variables de entorno.
"""

from pydantic_settings import BaseSettings
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    """Clase para definir las variables de entorno."""
    env_name: str = "Local"
    base_url: str = "http://127.0.0.1:8000"
    db_user: str = ""
    db_password: str = ""

    model_config = SettingsConfigDict(env_file='.env')


def get_settings() -> Settings:
    """Función que devuelve las variables de entorno, avisando en cuál entorno nos encontramos."""
    settings = Settings()
    print(f'Loading settings for {settings.env_name} environment.')
    return settings
