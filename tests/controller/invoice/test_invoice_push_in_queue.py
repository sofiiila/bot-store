import unittest
from unittest.mock import MagicMock, patch
from src.controller.invoice import Invoice, UserDocument, CategoriesEnum
from src.db_client.core import DbClient


class TestInvoice(unittest.TestCase):
    def setUp(self):
        self.data = MagicMock(spec=UserDocument)
        self.data.id = 123
        self.data.user_id = 1
        self.data.category = CategoriesEnum.NEW
        self.base_url = "http://example.com"
        self.is_overdue_time = False
        self.tmp_dir = "/tmp"
        self.db_client = MagicMock(spec=DbClient)

    @patch('src.controller.invoice.CrmApiClient')
    def test_good_case_push_in_queue(self, _):
        """
        Метод in_queue добавляет в очередь как ожидалось
        """
        invoice = Invoice(
            data=self.data,
            base_url=self.base_url,
            db_client=self.db_client,
            is_overdue_time=self.is_overdue_time,
            tmp_dir=self.tmp_dir
        )

        invoice.push_in_queue()

        self.db_client.update.assert_called_once_with(
            filter_query={"user_id": self.data.user_id, "id": self.data.id},
            value={"category": CategoriesEnum.QUEUE}
        )

    @patch('src.controller.invoice.CrmApiClient')
    def test_bad_case_push_in_queue_category_not_changed(self, _):
        """
        Метод in_queue не меняет категорию как ожидалось
        """
        invoice = Invoice(
            data=self.data,
            base_url=self.base_url,
            db_client=self.db_client,
            is_overdue_time=self.is_overdue_time,
            tmp_dir=self.tmp_dir
        )

        self.db_client.update.side_effect = lambda filter_query, value: None

        invoice.push_in_queue()

        self.db_client.update.assert_called_once_with(
            filter_query={"user_id": self.data.user_id, "id": self.data.id},
            value={"category": CategoriesEnum.QUEUE}
        )
        self.assertNotEqual(self.data.category, CategoriesEnum.QUEUE)


if __name__ == '__main__':
    unittest.main()
