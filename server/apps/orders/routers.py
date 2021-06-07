from fastapi import APIRouter
from datetime import datetime

from fastapi import HTTPException, status
from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse

from utils import parse_json
from .models import Order, Rentability
from apps.products.crud import find_product
from apps.clients.crud import find_client
from .crud import insert_order

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

@router.post('/create', response_description='Add new order', status_code=201)
async def create_order(order: Order):
    new_order = order.dict()
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
        
        # Calculate and imputes rentability
        rentability = calculate_rentability(item['unitary_price'], product_associated['unitary_price'])
        item['rentability'] = rentability
    
    # Tries to insert data in the db
    new_order = parse_json(new_order)
    created_order = await insert_order(new_order)
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_order)