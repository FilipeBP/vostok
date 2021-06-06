from pymongo import MongoClient

client = MongoClient('mongodb+srv://filipeUser:<password>@cluster0.tfv4a.mongodb.net/test')
db = client['mercosProject']
