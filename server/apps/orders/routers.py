from fastapi import APIRouter
from datetime import datetime

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder

from .models import Order, Rentability
from apps.products.crud import find_product
from apps.clients.crud import find_client
from .crud import find_order, insert_order, list_orders

router = APIRouter(
    prefix='/orders',
    tags=['orders']
)

def calculate_rentability(item_price, product_price):
    item_price, product_price = float(item_price), float(product_price)
    diff_percent = (product_price - item_price)/product_price * 100

    if diff_percent < 0:
        rentability = Rentability.excellent
    elif diff_percent <= 10:
        rentability = Rentability.good
    else:
        rentability = Rentability.bad
    return rentability

@router.get('/', response_description='List all orders')
async def get_orders(limit: int = 10):
    orders = await list_orders(limit)

    return orders

@router.get('/{id}', response_description='Get a order', response_model=Order)
async def get_order(id: str):
    return await find_order(id_order=id)


@router.post('/create', response_description='Add new order', status_code=201)
async def create_order(order: Order):
    new_order = jsonable_encoder(order)
    print(new_order)
    new_order['created_at'] = datetime.now()
    
    # Checks if the client exists in the clients collection
    await find_client(name=new_order['client'])
    
    for item in new_order['itens']:
        product = item['product']
        product_associated = await find_product(name=product)

        # Checks if the item quantity is multiple of the product stack size
        item_quantity = item['quantity']
        product_stack_size = product_associated['stack_size']
        if not item_quantity % product_stack_size == 0:
            detail_msg = f"The {product} quantity ({item_quantity}) has to be multiple of its stack size which is {product_stack_size}"
            raise HTTPException(status_code=412, detail=detail_msg)

        # Checks if rentability is empty
        if item['rentability']:
            raise HTTPException(status_code=412, detail=f"Rentability is only defined by the server")
        
        # Calculate and imputes rentability
        rentability = calculate_rentability(item['unitary_price'], product_associated['unitary_price'])
        item['rentability'] = rentability
    
    # Tries to insert data in the db
    created_order = await insert_order(new_order)
    return created_order