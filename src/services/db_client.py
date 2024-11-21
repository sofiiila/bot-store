from pymongo import MongoClient
from src.settings import settings


def get_db_client():
    client = MongoClient(f'mongodb://{settings.db_user}:{settings.db_password}@localhost:27017/')
    return client
