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

    def test_good_case_get_category(self):
        """
        Проверяет корректность работы метода get_category
        """
        user_id = 1
        mock_document = {"user_id": user_id, "category": "test_category"}

        with patch.object(self.db_client, '_DbClient__collection', self.mock_collection):
            self.mock_collection.find_one = MagicMock(return_value=mock_document)

            result = self.db_client.get_category(user_id)

            self.mock_collection.find_one.assert_called_once_with({"user_id": user_id})

            self.assertEqual(result, "test_category")

    def test_bad_case_get_category(self):
        """
        Проверяет выбрасываемого исключения метода get_category
    
        """
        user_id = 1

        with patch.object(self.db_client, '_DbClient__collection', self.mock_collection):
            self.mock_collection.find_one = MagicMock(return_value=None)

            with self.assertRaises(ValueError) as context:
                self.db_client.get_category(user_id)

            self.assertEqual(str(context.exception), f"Документ не найден с таким {user_id}")


if __name__ == '__main__':
    unittest.main()
