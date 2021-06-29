from typing import List
from fastapi import APIRouter
from datetime import datetime

from fastapi.encoders import jsonable_encoder
from fastapi import Response
from apps.orders.services import process_order

from utils import print_bold

from .models import Order
from apps.clients.crud import find_client
from .crud import delete_order, find_order, insert_order, list_orders

router = APIRouter(
    prefix='/orders',
    tags=['orders']
)


@router.get('/', response_description='List all orders', response_model=List[Order])
async def get_orders(limit: int = 10):
    orders = await list_orders(limit)

    return orders

@router.get('/{id}', response_description='Get a order', response_model=Order)
async def get_order(id: str):
    return await find_order(id_order=id)

@router.put('/{id}', response_description='Update a order', response_model=Order)
async def alter_order(id: str):
    pass
    # Checar ID e realizar validações igual do post

@router.delete('/{id}', response_description='Delete a order')
async def remove_order(id: str):
    #Tries to delete an order
    await delete_order(id)

    return Response(status_code=204)


@router.post('/create', response_description='Add new order', status_code=201)
async def create_order(order: Order):
    order.created_at = datetime.now()
    
    # Checks if the client exists in the clients collection
    await find_client(name=order.client)
    processed_order = await process_order(order)
    
    # Tries to insert data in the db
    processed_order = jsonable_encoder(processed_order)
    created_order = await insert_order(processed_order)
    
    return created_order
