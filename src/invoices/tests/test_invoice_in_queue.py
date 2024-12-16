import unittest
from unittest.mock import MagicMock, patch
from src.invoices.invoice import Invoice, Settings, UserDocument, CategoriesEnum


class TestInvoice(unittest.TestCase):
    def setUp(self):
        self.data = MagicMock(spec=UserDocument)
        self.data.user_id = 1
        self.data.id = 123
        self.settings = MagicMock(spec=Settings)
        self.settings.base_url = "http://example.com"
        self.db_client = MagicMock()

    @patch('src.invoices.invoice.CrmApiClient')
    def test_good_case_in_queue(self, _):
        """
        Метод in_queue добавляет в очередь как ожидалось
        """
        invoice = Invoice(self.data, self.settings.base_url, self.db_client)

        invoice.in_queue()

        self.db_client.update.assert_called_once_with(
            filter_query={"user_id": self.data.user_id, "id": self.data.id},
            value={"category": CategoriesEnum.QUEUE}
        )
# test_bad_case_invoice_in_queue не нужен т.к метод creater не выбрасывает исключение


if __name__ == '__main__':
    unittest.main()
