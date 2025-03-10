import unittest
from unittest.mock import MagicMock
from src.controller.invoice_look_up import InvoiceLookUp
from src.controller.invoice import Invoice, UserDocument
from src.db_client.db_client_types import CategoriesEnum


class TestInvoiceLookUp(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://example.com"
        self.is_overdue_time = False
        self.tmp_dir = "/tmp"
        self.db_client = MagicMock()
        self.invoice_lookup = InvoiceLookUp(self.base_url, self.db_client,
                                            self.is_overdue_time, self.tmp_dir)

    def test_good_case_get_all_new_invoices(self):
        """
        Вызывает метод get_all_new_invoices и проверяет, что он возвращает список Invoice объектов.
        """
        mock_data = [UserDocument(id="1", user_id="12345"), UserDocument(id="2", user_id="145")]
        self.db_client.list.return_value = mock_data

        result = self.invoice_lookup.get_all_new_invoices()

        self.assertEqual(len(result), len(mock_data))

        for invoice in result:
            self.assertIsInstance(invoice, Invoice)

        self.db_client.list.assert_called_once_with(
            filter_query={"category": CategoriesEnum.NEW}
        )

    def test_bad_case_get_all_new_invoices(self):
        """
        Вызывает метод get_all_new_invoices и проверяет, что он возвращает пустой список.
        """
        self.db_client.list.return_value = []

        result = self.invoice_lookup.get_all_new_invoices()

        self.assertEqual(len(result), 0)
        self.db_client.list.assert_called_once_with(
            filter_query={"category": CategoriesEnum.NEW}
        )


if __name__ == '__main__':
    unittest.main()
