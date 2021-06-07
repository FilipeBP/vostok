from database import db
from .models import Order

collection = db['orders']

async def insert_order(order: Order):
    new_order = await collection.insert_one(order)
    return await collection.find_one({'_id': new_order.inserted_id})