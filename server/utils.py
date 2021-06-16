from datetime import datetime
import json
from bson import ObjectId
from decimal import Decimal

from pydantic import BaseModel, Field

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
    id: AliasObjectId = Field(default_factory=AliasObjectId, alias='_id')

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {
            datetime: str,
            ObjectId: str
        }

class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        classes_to_parse = [ObjectId, Decimal, datetime]

        if any(filter(lambda x: isinstance(o, x), classes_to_parse)):
            return str(o)
        return json.JSONEncoder.default(self, o)

def parse_json(data):
    obj_parsed = JSONEncoder().encode(data)
    return json.loads(obj_parsed)

def print_bold(text: str, jump_n_lines_before: int = None, jump_n_lines_after: int = None):
    skip_line = '\n'
    if jump_n_lines_before:
        text = f"{jump_n_lines_before*skip_line}{text}"
    
    if jump_n_lines_after:
        text = f"{text}{jump_n_lines_after*skip_line}"
    
    print(f"\033[1m {text} \033[0m")
