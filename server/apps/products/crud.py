from database import db

async def list_products(limit_size: int = 10):
    return await db['products'].find().to_list(limit_size)