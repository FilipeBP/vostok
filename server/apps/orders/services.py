from apps.orders.exceptions import NotMulipleError, RentabilityError

from apps.products.models import Product
from apps.orders.models import Item, Order, Rentability
from apps.products.crud import find_product


async def process_order(new_order: Order):
    for item in new_order['itens']:
        associated_product = await get_associated_product(item)

        await check_quantity(item, associated_product)

        item['rentability'] = await get_rentability(item, associated_product)
    return new_order

async def get_associated_product(item: dict):
    return await find_product(name=item['product'])

# async def check_quantity(item: Item, product: Product):
#     if not item.quantity % product.stack_size == 0:
#         raise NotMulipleError(product.name, item.quantity, product.stack_size)

async def check_quantity(item: Item, product: Product):
    if not item['quantity'] % product['stack_size'] == 0:
        raise NotMulipleError(product['name'], item['quantity'], product['stack_size'])

# async def get_rentability(item: Item, product: Product):
#     rentability = calculate_rentability(item.unitary_price, product.unitary_price)

#     if item.rentability is not None and item.rentability != rentability:
#         raise RentabilityError()
#     return rentability

async def get_rentability(item: Item, product: Product):
    rentability = calculate_rentability(item['unitary_price'], product['unitary_price'])

    if item['rentability'] is not None and item['rentability'] != rentability:
        raise RentabilityError()
    return rentability

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
