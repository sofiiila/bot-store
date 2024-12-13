import unittest
from unittest.mock import MagicMock, patch
from src.invoices.invoice import Invoice, Settings, UserDocument


class TestInvoice(unittest.TestCase):
    def setUp(self):
        self.data = MagicMock(spec=UserDocument)
        self.settings = MagicMock(spec=Settings)
        self.db_client = MagicMock()

    @patch('src.invoices.invoice.CrmApiClient')
    @patch('src.invoices.invoice.Invoice.in_queue')
    def test_good_case_invoice_create(self, mock_in_queue, MockCrmApiClient):
        """
        Тестирует метод create класса Invoice
        """
        invoice = Invoice.create(self.data, self.settings, self.db_client)

        MockCrmApiClient.assert_called_once_with(self.settings)

        mock_in_queue.assert_called_once()

        self.assertIsInstance(invoice, Invoice)
# test_bad_case_invoice_create не нужен т.к метод creater не выбрасывает исключение


if __name__ == '__main__':
    unittest.main()
