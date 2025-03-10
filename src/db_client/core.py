"""
module core db_client
"""
import logging

import pymongo
from bson import ObjectId
from pymongo import MongoClient
from pymongo.results import UpdateResult, InsertOneResult

from src.db_client.db_client_types import UserDocument

logger = logging.getLogger(__name__)


class DbClient:
    """
    db client
    """
    def __init__(self, db_user, db_password, host='localhost', port=27017):
        connection_string = f'mongodb://{db_user}:{db_password}@{host}:{port}/'
        db_client = MongoClient(connection_string)
        # TODO задать более адекватные названия БД и название коллекции
        db = db_client["your_database"]
        self.__collection = db["mycollection"]

    def update_user_data(self, user_id, field, value):
        """
        ф-я обновляет данные
        :param user_id:
        :param field:
        :param value:
        :return:
        """
        self.__collection.update_one(
            {"user_id": user_id},
            {"$set": {field: value}}
        )

    def create(self, user_id) -> UserDocument:
        """
        метод открывающий заявку
        :param user_id:
        :return:
        """
        document = UserDocument.create_model(user_id).model_dump()
        document.pop('id')
        result: InsertOneResult = self.__collection.insert_one(document)
        return UserDocument(user_id=int(user_id), id=str(result.inserted_id))

    def get_category(self, user_id):
        """
        метод для получения категории документа
        :param user_id:
        :return: category
        """
        doc = self.__collection.find_one({"user_id": user_id})
        if doc is None:
            raise ValueError(f"Документ не найден с таким {user_id}")

        return doc.get("category")

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
        logger.info('ФИЛЬТРЫ %s', clean_filter_query)
        if result.modified_count == 0:
            raise AttributeError("Ничего не обновилось")

    #TODO переименуй методы, чтобы не пришлось тут комментировать pylint
    def list(self, filter_query: dict, sort_query: dict | None = None) -> list[UserDocument]:
        """
        Полученние списка документов из коллекции
        :param filter_query:  Это словарь, который используется для фильтрации
                                                        документов в коллекции.
               Каждый ключ и значение в этом словаре представляют собой поле и
                                    значение, которые должны быть в документе.
               sort_query: Это словарь, который используется для сортировки
               документов в коллекции. Каждый ключ и значение в этом словаре
                            представляют собой поле и направление сортировки.
               Если значение равно 1, то сортировка будет по возрастанию,
                а если значение равно -1, то сортировка будет по убыванию.
                Например, если sort_query равен {"user_id": 1}, то метод list
                  отсортирует документы по полю user_id в порядке возрастания.
        :return: results
        """
        cleaned_sort_query = {}
        if sort_query:
            for key, value in sort_query.items():
                if value == 1:
                    cleaned_sort_query[key] = pymongo.ASCENDING
                elif value == -1:
                    cleaned_sort_query[key] = pymongo.DESCENDING
                else:
                    raise ValueError("Не может быть другим значением")
        cleaned_filter_query = {}
        for key, value in filter_query.items():
            if key == "_id":
                cleaned_filter_query["_id"] = ObjectId(value)
            else:
                cleaned_filter_query[key] = value
        if cleaned_sort_query:
            documents = self.__collection.find(cleaned_filter_query).sort(cleaned_sort_query)
        else:
            documents = self.__collection.find(cleaned_filter_query)
        results = []
        for doc in documents:
            logger.debug("Документ %s", doc)
            results.append(UserDocument(**doc, id=str(doc["_id"])))
        return results

    #TODO переименуй методы, чтобы не пришлось тут комментировать pylint
    # pylint: disable=redefined-builtin
    def delete(self, id):
        """
        отработано
        :return:
        """
        result = self.__collection.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 0:
            raise ValueError(f"Документ с id не найден для удаления. {id}")
        logger.debug("Документ с id успешно удален. %s", id)
