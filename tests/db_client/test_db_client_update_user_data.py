import unittest
from unittest.mock import MagicMock, patch

from src.db_client.core import DbClient


class TestDbClient(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.patcher = patch('src.db_client.core.MongoClient')
        cls.MockMongoClient = cls.patcher.start()
        cls.mock_client = cls.MockMongoClient.return_value
        cls.mock_db = cls.mock_client["your_database"]
        cls.mock_collection = cls.mock_db["mycollection"]
        cls.db_client = DbClient(db_user='test_user', db_password='test_password')

    @classmethod
    def tearDownClass(cls):
        cls.patcher.stop()

    def test_good_case_update_user_data(self):
        """Проверяем корректность работы метода update_user_data"""
        user_id = 1
        field = 'name'
        value = 'John Doe'

        self.mock_collection.update_one = MagicMock(return_value=None)

        self.db_client.update_user_data(user_id, field, value)

        self.mock_collection.update_one.assert_called_once_with(
            {"user_id": user_id},
            {"$set": {field: value}}
        )

    def test_bad_case_update_user_data(self):
        """Проверяем, что метод update_user_data вызывает исключение,
        если метод update_one вызывает исключение"""
        user_id = 1
        field = 'name'
        value = 'John Doe'

        self.mock_collection.update_one = MagicMock(side_effect=Exception('Вызывается исключение'))

        with self.assertRaises(Exception):
            self.db_client.update_user_data(user_id, field, value)


if __name__ == '__main__':
    unittest.main()
