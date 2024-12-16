import unittest
from unittest.mock import MagicMock, patch

from src.invoices.invoice_look_up import InvoiceLookUp


class TestInvoiceLookUp(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://example.com"
        self.db_client = MagicMock()
        self.invoice_lookup = InvoiceLookUp(self.base_url, self.db_client)

    @patch('src.invoices.invoice_look_up.logger')
    def test_good_case_get_invoice_by_id(self, mock_logger):
        """Вызывает метод get_invoice_by_id и проверяет, что он возвращает объект Invoice."""
        mock_invoice_data = MagicMock()
        mock_invoice_data.id = "12345"
        self.db_client.list.return_value = [mock_invoice_data]

        result = self.invoice_lookup.get_invoice_by_id("12345")

        self.assertIsNotNone(result)
        self.db_client.list.assert_called_once_with(
            filter_query={"_id": "12345"}
        )
        mock_logger.debug.assert_called_once_with("получение заявки по id")

    def test_bad_case_get_invoice_by_id(self):
        """Вызывает метод get_invoice_by_id и проверяет, что он возвращает None."""
        self.db_client.list.return_value = []

        result = self.invoice_lookup.get_invoice_by_id("12345")

        self.assertIsNone(result)
        self.db_client.list.assert_called_once_with(
            filter_query={"_id": "12345"}
        )


if __name__ == '__main__':
    unittest.main()
