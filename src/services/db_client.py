from pymongo import MongoClient
from src.settings import settings


def get_db_client():
    client = MongoClient(f'mongodb://{settings.db_user}:{settings.db_password}@localhost:27017/')
    return client


def update_user_data(user_id, field, value):
    client = get_db_client()
    db = client['mydatabase']
    collection = db['mycollection']
    collection.update_one(
        {"user_id": user_id},
        {"$set": {field: value}}
    )