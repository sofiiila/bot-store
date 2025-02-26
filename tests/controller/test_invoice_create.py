import unittest
from unittest.mock import MagicMock, patch
from src.controller.invoice import Invoice, UserDocument, DbClient


class TestInvoice(unittest.TestCase):
    def setUp(self):
        self.user_id = 1 
        self.base_url = "http://example.com"
        self.is_overdue_time = False
        self.tmp_dir = "/tmp"
        self.db_client = MagicMock(spec=DbClient)

    @patch('src.controller.invoice.CrmApiClient')
    def test_good_case_invoice_create(self, MockCrmApiClient):
        """
        Тестирует метод create класса Invoice
        """
        mock_data = MagicMock(spec=UserDocument)
        self.db_client.create.return_value = mock_data

        invoice = Invoice.create(
            db_client=self.db_client,
            user_id=self.user_id,
            base_url=self.base_url,
            is_overdue_time=self.is_overdue_time,
            tmp_dir=self.tmp_dir
        )

        MockCrmApiClient.assert_called_once_with(self.base_url)

        self.assertIsInstance(invoice, Invoice)


if __name__ == '__main__':
    unittest.main()