import unittest
from unittest.mock import MagicMock, patch
from datetime import datetime, timedelta
from src.invoices.invoice import Invoice, Settings, UserDocument


class TestInvoice(unittest.TestCase):
    def setUp(self):
        self.data = MagicMock(spec=UserDocument)
        self.data.id = 123
        self.data.start_date = datetime.now() - timedelta(minutes=40)  
        self.settings = MagicMock(spec=Settings)
        self.settings.base_url = "http://example.com"
        self.db_client = MagicMock()

    @patch('src.invoices.invoice.CrmApiClient')
    def test_good_case_is_overdue(self, MockCrmApiClient):
        """
        Метод в случае когда заявка пролежала больше 30минут
        """
        invoice = Invoice(self.data, self.settings.base_url, self.db_client)

        result = invoice.is_overdue()

        self.assertTrue(result)

    @patch('src.invoices.invoice.CrmApiClient')
    def test_bad_case_is_overdue(self, MockCrmApiClient):
        """
        Когда заявка не просрочена
        """
        self.data.start_date = datetime.now() - timedelta(minutes=20) 
        invoice = Invoice(self.data, self.settings.base_url, self.db_client)

        result = invoice.is_overdue()

        self.assertFalse(result)


if __name__ == '__main__':
    unittest.main()
