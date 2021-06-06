import motor.motor_asyncio
import json

DB_URL = 'mongodb+srv://filipeUser:LeArNiNg10!!@cluster0.tfv4a.mongodb.net/test'

client = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
db = client['mercosProject']