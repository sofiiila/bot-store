import unittest
from unittest.mock import MagicMock, patch
from bson import ObjectId
import pymongo
from src.db_client.core import DbClient, UserDocument


class TestDbClient(unittest.TestCase):

    @patch('src.db_client.core.MongoClient')
    def setUp(self, MockMongoClient):
        self.mock_client = MockMongoClient.return_value
        self.mock_db = self.mock_client["your_database"]
        self.mock_collection = self.mock_db["mycollection"]
        self.db_client = DbClient(db_user='test_user', db_password='test_password')

    def test_good_case_list(self):
        """
        Проверяет успешное получение списка документов из БД
        """
        filter_query = {"_id": "a1b2c3d4e5f6a1b2c3d4e5f6"}
        sort_query = {"field": 1}
        mock_documents = [
            {"_id": ObjectId("a1b2c3d4e5f6a1b2c3d4e5f6"), "field": "value1", "user_id": 1},
            {"_id": ObjectId("a1b2c3d4e5f6a1b2c3d4e5f7"), "field": "value2", "user_id": 2}
        ]
        expected_results = [
            UserDocument(user_id=1, id="a1b2c3d4e5f6a1b2c3d4e5f6", field="value1"),
            UserDocument(user_id=2, id="a1b2c3d4e5f6a1b2c3d4e5f7", field="value2")
        ]

        with patch.object(self.db_client, '_DbClient__collection', self.mock_collection):
            mock_cursor = MagicMock()
            mock_cursor.sort = MagicMock(return_value=mock_documents)
            self.mock_collection.find = MagicMock(return_value=mock_cursor)

            results = self.db_client.list(filter_query, sort_query)

            cleaned_filter_query = {"_id": ObjectId(filter_query["_id"])}
            cleaned_sort_query = {"field": pymongo.ASCENDING}
            self.mock_collection.find.assert_called_once_with(cleaned_filter_query)
            mock_cursor.sort.assert_called_once_with(cleaned_sort_query)

            self.assertEqual(results, expected_results)

    def test_bad_case_list(self):
        """
        Проверяет случай, когда sort_query имеет недопустимое значение
        """
        filter_query = {"_id": "a1b2c3d4e5f6a1b2c3d4e5f6"}
        sort_query = {"field": 2}

        with patch.object(self.db_client, '_DbClient__collection', self.mock_collection):

            with self.assertRaises(ValueError) as context:
                self.db_client.list(filter_query, sort_query)

            self.assertEqual(str(context.exception), "Не может быть другим значением")


if __name__ == '__main__':
    unittest.main()
