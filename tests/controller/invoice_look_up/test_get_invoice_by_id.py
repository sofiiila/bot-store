import unittest
from unittest.mock import MagicMock, patch
from src.controller.invoice_look_up import InvoiceLookUp
from src.controller.invoice import Invoice


class TestInvoiceLookUp(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://example.com"
        self.is_overdue_time = False
        self.tmp_dir = "/tmp"
        self.db_client = MagicMock()
        self.invoice_lookup = InvoiceLookUp(self.base_url, self.db_client,
                                            self.is_overdue_time, self.tmp_dir)

    @patch('src.controller.invoice_look_up.logger')
    @patch.object(InvoiceLookUp, '_construct_invoice')
    def test_good_case_get_invoice_by_id(self, mock_construct_invoice, mock_logger):
        """
        Вызывает метод get_invoice_by_id и проверяет, что он возвращает объект Invoice.
        """
        mock_invoice_data = MagicMock()
        mock_invoice_data.id = "12345"
        self.db_client.list.return_value = [mock_invoice_data]

        mock_construct_invoice.return_value = Invoice(
            data=mock_invoice_data,
            base_url=self.base_url,
            db_client=self.db_client,
            is_overdue_time=self.is_overdue_time,
            tmp_dir=self.tmp_dir
        )

        result = self.invoice_lookup.get_invoice_by_id("12345")

        self.assertIsInstance(result, Invoice)
        self.db_client.list.assert_called_once_with(
            filter_query={"_id": "12345"}
        )
        mock_logger.debug.assert_called_once_with("получение заявки по id")
        mock_construct_invoice.assert_called_once_with(mock_invoice_data)

    def test_bad_case_get_invoice_by_id(self):
        """
        Вызывает метод get_invoice_by_id и проверяет, что он возвращает None.
        """
        self.db_client.list.return_value = []

        result = self.invoice_lookup.get_invoice_by_id("12345")

        self.assertIsNone(result)
        self.db_client.list.assert_called_once_with(
            filter_query={"_id": "12345"}
        )


if __name__ == '__main__':
    unittest.main()
