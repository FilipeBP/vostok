from fastapi import APIRouter
from ..database import db

router = APIRouter(
    prefix='/clients',
    tags=['clients']
)

@router.get('/', response_description='Listing all clients')
async def list_clients(limit_size: int = 1000):
    clients = await db['clients'].find(projection={'_id': False}) \
                .to_list(limit_size)
    return clients