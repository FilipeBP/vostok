from fastapi import FastAPI
from orders.routers import client, product

app = FastAPI()

app.include_router(client.router)
app.include_router(product.router)

@app.get('/')
def index():
    return 'Initial page'
