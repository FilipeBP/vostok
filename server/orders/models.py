from pydantic import BaseModel, Field, condecimal
from bson import ObjectId
from typing import Optional

# MongoDB needs an '_id' field, however pydantic doesn't allow variables starting with '_'
class AliasObjectId(ObjectId):
    
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    # Checks if the data received is valid
    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError('Invalid ObjectId')
        return v

    # Avoid an error when accessing the documentation
    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type='string')

class Client(BaseModel):
    id: Optional[AliasObjectId] = Field(alias='_id')
    name: str

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra = {
            "example": {
                "name": "Michael Mars"
            }
        }

class Product(BaseModel):
    id: Optional[AliasObjectId] = Field(alias='_id')
    name: str
    unitary_price: condecimal(decimal_places=2)
    stack_size: int = Field(gt=0)

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }
        schema_extra = {
            "example": {
                "name": "Doll",
                "unitary_price": 310.00,
                "stack_size": 2
            }
        }