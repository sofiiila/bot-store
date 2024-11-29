from pymongo import MongoClient


class DbClient:
    def __init__(self, db_user, db_password, host='localhost', port=27017):
        connection_string = f'mongodb://{db_user}:{db_password}@{host}:{port}/'
        db_client = MongoClient(connection_string)
        db = db_client["your_database"]
        self.__collection = db["mycollection"]

    def update_user_data(self, user_id, field, value):
        self.__collection.update_one(
            {"user_id": user_id},
            {"$set": {field: value}}
        )

    def get_user_state(self, user_id):
        user_data = self.__collection.find_one({"user_id": user_id})
        return user_data.get('state', None) if user_data else None

    def set_user_state(self, user_id, state):
        self.__collection.update_one(
            {"user_id": user_id},
            {"$set": {"state": state}},
            upsert=True
        )

    def create(self, user_id):
        document = {
            "user_id": user_id,
            "question": "No question",
            "tz": "No TZ",
            "files": "No files",
            "deadline": "No deadline",
            "contacts": "No contacts",
        }
        self.__collection.insert_one(document)

