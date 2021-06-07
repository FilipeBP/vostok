from pydantic import (
    BaseModel,
    Field,
    validator,
    condecimal
)

from utils import AliasObjectId, MongoBaseModel
from typing import List, Optional
from enum import Enum
from datetime import datetime

class Rentability(str, Enum):
    excellent = 'excellent'
    good = 'good'
    bad = 'bad'

class Item(BaseModel):
    product: str
    quantity: int = Field(gt=0)
    unitary_price: condecimal(decimal_places=2)
    rentability: Optional[Rentability]

    @validator('unitary_price')
    def must_be_above_zero(cls, v):
        if v <= 0:
            raise ValueError('Unitary price must be greater than zero')
        return v

    @validator('rentability', pre=True, always=True)
    def must_be_none(cls, v):
        if v is not None:
            raise ValueError('Rentability is a field calculated by the server')
        return v



class Order(MongoBaseModel):
    id: Optional[AliasObjectId] = Field('_id')
    client: str
    itens: List[Item]
    created_at: Optional[datetime]

    class Config:
        schema_extra = {
            "example": {
                "client": "Yoda Master",
                "itens": [
                    {
                    "product": "X-Wing",
                    "quantity": "6",
                    "unitary_price": 60001
                    },
                    {
                    "product": "Millenium Falcom",
                    "quantity": "1",
                    "unitary_price": 400000.65
                    }
                ]
            }
        }