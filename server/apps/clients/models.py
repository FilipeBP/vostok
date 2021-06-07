from utils import MongoBaseModel

class Client(MongoBaseModel):
    name: str

    class Config:
        schema_extra = {
            "example": {
                "name": "Michael Mars"
            }
        }
