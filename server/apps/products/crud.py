from database import db
from fastapi import HTTPException

collection = db['products']

async def list_products(limit_size: int = 10):
    return await collection.find().to_list(limit_size)

async def find_product(id_product: str = None, name: str = None):
    if not id_product and not name:
        raise ValueError("It's necessary to provide at least one identifier")
    
    if name:
        product = await collection.find_one(filter={'name': name})
    elif id_product:
        product = await collection.find_one(filter={'name': name})

    if product:
        return product

    detail_msg = f"Product {id_product if id_product else name} not found"
    raise HTTPException(status_code=404, detail=detail_msg)