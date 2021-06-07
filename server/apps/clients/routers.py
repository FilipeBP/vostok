from typing import List
from fastapi import APIRouter
from fastapi.encoders import jsonable_encoder

from .crud import find_client, insert_client, list_clients
from .models import Client


router = APIRouter(
    prefix='/clients',
    tags=['clients']
)

@router.get('/', response_description='Listing all clients', response_model=List[Client])
async def get_clients(limit_size: int = 10):
    clients = await list_clients(limit_size)
    return clients

@router.post(
    '/', response_description='Add a new client', status_code=201, response_model=Client
)
async def create_client(client: Client):
    client = jsonable_encoder(client)
    created_client = await insert_client(client)
    return created_client


@router.get('/{id}', response_description='Get a client', response_model=Client)
async def get_client(id: str):
    return await find_client(id_client=id)