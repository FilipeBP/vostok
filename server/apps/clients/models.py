from bson import ObjectId
from typing import Optional
from pydantic import Field

from utils import AliasObjectId, MongoBaseModel

class Client(MongoBaseModel):
    id: Optional[AliasObjectId] = Field(alias='_id')
    name: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Michael Mars"
            }
        }
