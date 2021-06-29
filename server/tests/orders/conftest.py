import sys
import os
import pytest

sys.path.append(os.getcwd())
print(sys.path)

from apps.orders.models import Rentability

@pytest.fixture
def item_success():
    return {'product': 'X-Wing', 'quantity': 6, 'unitary_price': 60001, 'rentability': None}

@pytest.fixture
def item_error():
    return {'product': 'X-Wing', 'quantity': 6, 'unitary_price': 60001, 'rentability': Rentability.bad}

@pytest.fixture
def product():
    return {'_id': '60bd84c9e9883cc11527b716', 'name': 'X-Wing', 'unitary_price': 60000.0, 'stack_size': 2}