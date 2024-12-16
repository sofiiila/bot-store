import unittest
from unittest.mock import MagicMock, patch
from pymongo.results import UpdateResult
from bson import ObjectId
from src.services.core import DbClient


class TestDbClient(unittest.TestCase):

    def setUp(self):
        with patch('src.services.core.MongoClient') as mock_mongo_client:
            self.mock_client = mock_mongo_client.return_value
            self.mock_db = self.mock_client["your_database"]
            self.mock_collection = self.mock_db["mycollection"]
            self.db_client = DbClient(
                db_user='test_user',
                db_password='test_password')

    def test_good_case_update(self):
        """
        Проверяет успешное обновление документа в БД
        """
        filter_query = {"id": "60d5b524b8d6c9b34a7d2c7d"}
        value = {"status": "updated"}
        mock_update_result = MagicMock(spec=UpdateResult)
        mock_update_result.modified_count = 1

        with patch.object(self.db_client, '_DbClient__collection', self.mock_collection):
            self.mock_collection.update_one = MagicMock(return_value=mock_update_result)

            self.db_client.update(filter_query, value)

            clean_filter_query = {"_id": ObjectId(filter_query["id"])}
            self.mock_collection.update_one.assert_called_once_with(
                filter=clean_filter_query,
                update={"$set": value}
            )

    def test_bad_case_update(self):
        """
        Проверяет случай, когда ничего не обновилось
        """
        filter_query = {"id": "60d5b524b8d6c9b34a7d2c7d"}
        value = {"status": "updated"}
        mock_update_result = MagicMock(spec=UpdateResult)
        mock_update_result.modified_count = 0

        with patch.object(self.db_client, '_DbClient__collection', self.mock_collection):
            self.mock_collection.update_one = MagicMock(return_value=mock_update_result)

            with self.assertRaises(AttributeError) as context:
                self.db_client.update(filter_query, value)

            self.assertEqual(str(context.exception), "Ничего не обновилось")


if __name__ == '__main__':
    unittest.main()
