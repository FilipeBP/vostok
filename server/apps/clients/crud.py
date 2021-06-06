from database import db

async def list_clients(limit_size: int = 10):
    return await db['clients'].find().to_list(limit_size)