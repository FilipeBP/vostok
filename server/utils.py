import json
from bson import ObjectId, json_util
from pydantic.main import BaseModel

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

class MongoBaseModel(BaseModel):
    class Config:
        arbitrary_types_allowed = True
        json_encoders = {
            ObjectId: str
        }

def parse_json(data):
    return json.loads(json_util.dumps(data))