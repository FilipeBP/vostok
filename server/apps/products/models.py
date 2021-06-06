from utils import AliasObjectId, MongoBaseModel

from pydantic.types import condecimal
from typing import Optional
from pydantic import Field

class Product(MongoBaseModel):
    name: str
    unitary_price: condecimal(decimal_places=2)
    id: Optional[AliasObjectId] = Field(alias='_id')
    stack_size: int = Field(1, gt=0)

    class Config:
        schema_extra = {
            "example": {
                "name": "Doll",
                "unitary_price": 310.00,
                "stack_size": 2
            }
        }
