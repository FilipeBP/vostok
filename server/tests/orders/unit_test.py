import sys
import os
import pytest

sys.path.append(os.getcwd())
print(sys.path)

from apps.orders.models import Rentability
from apps.orders.services import calculate_rentability, get_rentability
from apps.orders.exceptions import RentabilityError

def test_calculate_rentability_success():
    assert calculate_rentability(130, 120) == Rentability.excellent
    assert calculate_rentability(100, 105) == Rentability.good
    assert calculate_rentability(100, 120) == Rentability.bad

@pytest.mark.asyncio
async def test_get_rentability_success(item_success, product):
    assert await get_rentability(item_success, product) is not None

@pytest.mark.asyncio
async def test_get_rentability_fail(item_error, product):
    with pytest.raises(RentabilityError):
        await get_rentability(item_error, product)
