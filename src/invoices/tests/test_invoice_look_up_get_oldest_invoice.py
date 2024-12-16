import unittest
from unittest.mock import MagicMock, patch

from src.invoices.invoice_look_up import InvoiceLookUp
from src.services.db_client_types import CategoriesEnum


class TestInvoiceLookUp(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://example.com"
        self.db_client = MagicMock()
        self.invoice_lookup = InvoiceLookUp(self.base_url, self.db_client)

    @patch('src.invoices.invoice_look_up.logger')
    def test_good_case_get_oldest_invoice(self, mock_logger):
        """
        Вызывает метод get_oldest_invoice и проверяет,
        что он возвращает объект Invoice.
        """
        mock_invoice_data = MagicMock()
        mock_invoice_data.id = "12345"
        self.db_client.list.return_value = [mock_invoice_data]

        result = self.invoice_lookup.get_oldest_invoice()

        self.assertIsNotNone(result)
        self.db_client.list.assert_called_once_with(
            filter_query={"category": CategoriesEnum.QUEUE},
            sort_query={"start_date": 1}
        )
        mock_logger.debug.assert_called_once_with("Получена заявка с ID: %s", "12345")

    def test_bad_case_get_oldest_invoice_bad_case(self):
        """
        Вызывает метод get_oldest_invoice и проверяет, что он возвращает None.
        """
        self.db_client.list.return_value = []

        result = self.invoice_lookup.get_oldest_invoice()

        self.assertIsNone(result)
        self.db_client.list.assert_called_once_with(
            filter_query={"category": CategoriesEnum.QUEUE},
            sort_query={"start_date": 1}
        )


if __name__ == '__main__':
    unittest.main()
