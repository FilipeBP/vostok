from fastapi import APIRouter
from ..database import db

router = APIRouter(
    prefix='/products',
    tags=['products']
)

@router.get('/', response_description='List all products')
async def list_products(limit_size: int = 1000):
    products = await db['products'].find(projection={'_id': False}) \
                .to_list(limit_size)
    return products

