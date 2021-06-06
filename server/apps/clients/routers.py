from typing import List
from fastapi import APIRouter

from .crud import list_clients
from .models import Client


router = APIRouter(
    prefix='/clients',
    tags=['clients']
)

@router.get('/', response_description='Listing all clients', response_model=List[Client])
async def get_clients(limit_size: int = 10):
    clients = await list_clients(limit_size)
    return clients