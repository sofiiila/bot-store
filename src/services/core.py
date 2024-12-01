import logging
from datetime import datetime

import pymongo
from bson import ObjectId
from pymongo import MongoClient
from pymongo.results import UpdateResult, InsertOneResult

from src.services.db_client_types import UserDocument

logger = logging.getLogger(__name__)


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

    def create(self, user_id) -> UserDocument:
        document = UserDocument.create_model(user_id).dict()
        document.pop('id')
        result: InsertOneResult = self.__collection.insert_one(document)
        return UserDocument(user_id=int(user_id), id=str(result.inserted_id))

    def get_category(self, user_id):
        """
        метод для получения категории документа
        :param user_id:
        :return: category
        """
        doc = self.__collection.find_one({"user_id": {user_id}})
        if doc is not None:
            return doc.get("category")
        else:
            raise ValueError(f"Документ не найден с таким {user_id}")

    def update(self, filter_query: dict, value: dict):
        """
        перевод в очередь, смена состояний записи в бд
        :return:
        """
        clean_filter_query = {}
        for key, dict_value in filter_query.items():
            if key == "id":
                clean_filter_query["_id"] = ObjectId(dict_value)
            else:
                clean_filter_query[key] = dict_value
        result: UpdateResult = self.__collection.update_one(
            filter=clean_filter_query,
            update={"$set": value}
        )
        if result.modified_count == 0:
            raise AttributeError("Ничего не обновилось")

    def list(self, filter_query: dict, sort_query: dict | None = None) -> list[UserDocument]:
        """
        фильтрация  в очереди
        :return:
        """
        cleaned_sort_query = {}
        for key, value in sort_query.items():
            if value == 1:
                cleaned_sort_query[key] = pymongo.ASCENDING
            elif value == -1:
                cleaned_sort_query[key] = pymongo.DESCENDING
            else:
                raise ValueError("Не может быть другим значением ")
        cleaned_filter_query = {}
        for key, value in filter_query.items():
            if key == "_id":
                cleaned_filter_query["_id"] = ObjectId(value)
            else:
                cleaned_filter_query[key] = value

        documents = self.__collection.find(cleaned_filter_query).sort(cleaned_sort_query or {})
        results = []
        for doc in documents:
            results.append(UserDocument(**doc, id=str(doc["_id"])))
        return results #TODO парсинг модели в тип UserDocument

    def delete(self, user_id, status=None):
        """
        отработано
        :return:
        """
        if status == "completed":
            self.queue_collection.delete_one({"user_id": user_id})
