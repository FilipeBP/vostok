from fastapi import APIRouter
from server.database import db
from ..models import Product
from typing import List

router = APIRouter(
    prefix='/products',
    tags=['products']
)

@router.get('/', response_description='List all products', response_model=List[Product])
async def list_products(limit: int = 1000):
    products = await db['products'].find().to_list(limit)
    return products

