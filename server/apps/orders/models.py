from pydantic import BaseModel, Field, condecimal

from utils import AliasObjectId, MongoBaseModel
from typing import List, Optional
from enum import Enum
from datetime import datetime

class Rentability(str, Enum):
    excellent = 'excellent'
    good = 'good'
    bad = 'bad'

class Item(BaseModel):
    name: str
    unitary_price: condecimal(decimal_places=2)
    quantity: int = Field(gt=0)
    rentability: Rentability


class Order(MongoBaseModel):
    id: Optional[AliasObjectId] = Field('_id')
    client: str
    itens: List[Item]
    created_at: datetime

    class Config:
        schema_extra = {
            "example": {
                "client": "Client.name",
                "products": [
                    {
                        "product": "Doll",
                        "quantity": "6",
                        "unitary_price": 320.00,
                        "rentability": "excellent"
                    }
                ],
            }
        }