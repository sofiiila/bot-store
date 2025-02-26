import unittest
from unittest.mock import MagicMock, patch

from src.db_client.core import DbClient


class TestDbClient(unittest.TestCase):

    @patch('src.db_client.core.MongoClient')
    def setUp(self, MockMongoClient):
        self.mock_client = MockMongoClient.return_value
        self.mock_db = self.mock_client["your_database"]
        self.mock_collection = self.mock_db["mycollection"]
        self.db_client = DbClient(db_user='test_user', db_password='test_password')

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