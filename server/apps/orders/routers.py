from fastapi import APIRouter
from datetime import datetime

from fastapi import HTTPException

from .models import Order, Rentability
from apps.products.crud import find_product

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

@router.post('/create', response_description='Add new order')
async def create_order(order: Order):
    new_order = order.dict()
    new_order['created_at'] = datetime.now()
    
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
    print(new_order)
    return new_order