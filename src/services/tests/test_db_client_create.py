import unittest
from unittest.mock import MagicMock, patch

from pymongo.results import InsertOneResult
from src.services.core import DbClient
from src.services.db_client_types import UserDocument


class TestDbClient(unittest.TestCase):

    def setUp(self):
        with patch('src.services.core.MongoClient') as mock_mongo_client:
            self.mock_client = mock_mongo_client.return_value
            self.mock_db = self.mock_client["your_database"]
            self.mock_collection = self.mock_db["mycollection"]
            self.db_client = DbClient(
                db_user='test_user',
                db_password='test_password')

    def test_good_case_create(self):
        """
        Проверяю, что метод create создает документ в БД
        """
        user_id = 1
        mock_insert_result = MagicMock(spec=InsertOneResult)
        mock_insert_result.inserted_id = 'mock_id'

        with patch.object(self.db_client, '_DbClient__collection', self.mock_collection):
            self.mock_collection.insert_one = MagicMock(return_value=mock_insert_result)

            result = self.db_client.create(user_id)

            expected_document = UserDocument.create_model(user_id).dict()
            expected_document.pop('id')
            self.mock_collection.insert_one.assert_called_once_with(expected_document)

            self.assertEqual(result.user_id, user_id)
            self.assertEqual(result.id, 'mock_id')

    def test_bad_case_create(self):
        """
        Проверяю, что метод create вызывает исключение, если в БД уже есть пользователь с таким id
        или если при подключении к БД произошла ошибка
        """
        user_id = 1

        with patch.object(self.db_client, '_DbClient__collection', self.mock_collection):
            self.mock_collection.insert_one = MagicMock(side_effect=Exception('Исключение'))

            with self.assertRaises(Exception):
                self.db_client.create(user_id)


if __name__ == '__main__':
    unittest.main()
