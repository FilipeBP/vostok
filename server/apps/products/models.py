from utils import MongoBaseModel

from pydantic.types import condecimal
from pydantic import Field

class Product(MongoBaseModel):
    name: str
    unitary_price: condecimal(decimal_places=2)
    stack_size: int = Field(1, gt=0)

    class Config:
        schema_extra = {
            "example": {
                "name": "Doll",
                "unitary_price": 310.00,
                "stack_size": 2
            }
        }
