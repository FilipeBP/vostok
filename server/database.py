import motor.motor_asyncio
from config import settings

DB_URL = f'mongodb+srv://{settings.db_user}:{settings.db_password}@cluster0.tfv4a.mongodb.net/test'

client = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
db = client['mercosProject']