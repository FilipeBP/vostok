from fastapi.exceptions import HTTPException
from starlette.responses import JSONResponse

from database import db
from .models import Order

collection = db['orders']

async def insert_order(order: Order):
    new_order = await collection.insert_one(order)
    return await collection.find_one({'_id': new_order.inserted_id})

async def list_orders(limit_size: int = 10):
    return await collection.find().to_list(limit_size)

async def find_order(id_order: str = None, name: str = None):
    if not id_order and not name:
        raise ValueError("It's necessary to provide at least one identifier")
    
    if name:
        order = await collection.find_one(filter={'name': name})
    elif id_order:
        order = await collection.find_one(filter={'_id': id_order})

    if order:
        return order

    detail_msg = f"order {id_order if id_order else name} not found"
    raise HTTPException(status_code=404, detail=detail_msg)

async def delete_order(id: str):
    deleted_order = await collection.delete_one({'_id': id})
    print(deleted_order)

    if deleted_order.deleted_count == 0:
        detail_msg = f'Order {id} was not found.'
        raise HTTPException(status_code=404, detail=detail_msg)