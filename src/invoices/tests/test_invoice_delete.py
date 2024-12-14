import unittest
from unittest.mock import MagicMock, patch
from src.invoices.invoice import Invoice, Settings, UserDocument


class TestInvoice(unittest.TestCase):
    def setUp(self):
        self.data = MagicMock(spec=UserDocument)
        self.data.id = 123
        self.settings = MagicMock(spec=Settings)
        self.settings.base_url = "http://example.com"
        self.db_client = MagicMock()

    @patch('src.invoices.invoice.CrmApiClient')
    def test_good_case_delete(self, _):
        """
        Заявка удаляется из базы данных
        """
        invoice = Invoice(self.data, self.settings.base_url, self.db_client)

        invoice.delete()

        self.db_client.delete.assert_called_once_with(self.data.id)


if __name__ == '__main__':
    unittest.main()
