import unittest
from unittest.mock import MagicMock, patch

from bson import ObjectId
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

    def test_good_case_delete(self):
        """
        Проверяет успешное удаление документа из БД
        """
        doc_id = "a1b2c3d4e5f6a1b2c3d4e5f6"
        mock_delete_result = MagicMock()
        mock_delete_result.deleted_count = 1

        with patch.object(self.db_client, '_DbClient__collection', self.mock_collection):
            self.mock_collection.delete_one = MagicMock(return_value=mock_delete_result)

            self.db_client.delete(doc_id)

            self.mock_collection.delete_one.assert_called_once_with({'_id': ObjectId(doc_id)})

    def test_bad_case_delete(self):
        """
        Проверяет случай, когда документ не найден для удаления
        """
        doc_id = "60d5b524b8d6c9b34a7d2c7d"
        mock_delete_result = MagicMock()
        mock_delete_result.deleted_count = 0

        with patch.object(self.db_client, '_DbClient__collection', self.mock_collection):
            self.mock_collection.delete_one = MagicMock(return_value=mock_delete_result)

            with self.assertRaises(ValueError) as context:
                self.db_client.delete(doc_id)

            self.assertEqual(str(context.exception),
                             f"Документ с id не найден для удаления. {doc_id}")
