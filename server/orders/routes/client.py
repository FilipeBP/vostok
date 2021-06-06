from fastapi import APIRouter
from server.database import db
from ..models import Client
from typing import List

router = APIRouter(
    prefix='/clients',
    tags=['clients']
)

@router.get('/', response_description='Listing all clients', response_model=List[Client])
async def list(limit: int = 1000):
    clients = await db['clients'].find().to_list(limit)
    return clients