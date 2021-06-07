from fastapi import HTTPException
from database import db

collection = db['clients']

async def list_clients(limit_size: int = 10):
    return await collection.find().to_list(limit_size)

async def find_client(id_client: str = None, name: str = None):
    if not id_client and not name:
        raise ValueError("It's necessary to provide at least one identifier")
    
    if name:
        client = await collection.find_one(filter={'name': name})
    elif id_client:
        client = await collection.find_one(filter={'_id': id_client})

    if client:
        return client

    detail_msg = f"Client {id_client if id_client else name} not found"
    raise HTTPException(status_code=404, detail=detail_msg)

async def insert_client(client: dict):
    new_client = await collection.insert_one(client)
    return await collection.find_one({'_id': new_client.inserted_id})