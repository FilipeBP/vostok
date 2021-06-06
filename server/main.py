from fastapi import FastAPI
from database import db
import os
import json

from apps.clients.routers import router as client_router
from apps.products.routers import router as product_router

app = FastAPI()

app.include_router(client_router)
app.include_router(product_router)

async def filling_collection(collection_name, file_name):
    collections = await db.list_collections()
    collections_filtered = filter(lambda x: x['name'] == collection_name, collections)
    if len(list(collections_filtered)) > 0:
        return

    file = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', file_name))
    with open(file) as f:
        data = json.load(f)
        await db[collection_name].insert_many(data)
        print(f'Inserted data to {collection_name} with success')

@app.on_event('startup')
async def filling_collections():
    await filling_collection('clients', 'clients.json')
    await filling_collection('products', 'products.json')
    

@app.get('/')
def index():
    return 'Initial page'
