from .models import Product
from .crud import list_products

from typing import List
from fastapi import APIRouter

router = APIRouter(
    prefix='/products',
    tags=['products']
)

@router.get('/', response_description='List all products', response_model=List[Product])
async def get_products(limit_size: int = 10):
    products = await list_products(limit_size)

    return products

