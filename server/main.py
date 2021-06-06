from fastapi import FastAPI
from orders.routers import client, product
from orders.database import db
import os
import json

app = FastAPI()

app.include_router(client.router)
app.include_router(product.router)

async def filling_collection(collection_name, file_name):
    collections = await db.list_collections()
    if len(list(filter(lambda x: x['name'] == collection_name, collections))) > 0:
        return

    file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', file_name))
    with open(file) as f:
        data = json.load(f)
        await db[collection_name].insert_many(data)

@app.on_event('startup')
async def filling_collections():
    await filling_collection('clients', 'clients.json')
    await filling_collection('products', 'products.json')
    

@app.get('/')
def index():
    return 'Initial page'
