"""Aprendiendo a usar FastAPI.
Este archivo sólo sirve para manejo de las rutaas de la API.

Esta ruta se activa desde main.
"""

from fastapi import APIRouter


# Instancia de la ruta de la API
router = APIRouter(
    prefix='/products',
    tags=['Products'],
    responses={404: {'message': 'Producto no encontrado'}},
)


# Datos para ser consultados
products: list[str] = ["Producto 1", "Producto 2", "Producto 3", "Producto 4"]

# Endpoints de la ruta
@router.get(path='/')
async def show_products():
    """Muestra una lista de productos."""
    return products

@router.get(path='/{product_id}')
async def product_by_id(product_id: int):
    """Busca un producto por su ubicación como número de id."""
    return products[product_id]
