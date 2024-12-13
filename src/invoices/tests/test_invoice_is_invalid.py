import unittest
from unittest.mock import MagicMock, patch
from src.invoices.invoice import Invoice, Settings, UserDocument, CategoriesEnum


class TestInvoice(unittest.TestCase):
    def setUp(self):
        self.data = MagicMock(spec=UserDocument)
        self.data.id = 123
        self.settings = MagicMock(spec=Settings)
        self.settings.base_url = "http://example.com"
        self.db_client = MagicMock()

    @patch('src.invoices.invoice.CrmApiClient')
    def test_good_case_is_invalid(self, MockCrmApiClient):
        """
        Метод __is_invalid добавляет категорию is_invalid в БД
        """
        invoice = Invoice(self.data, self.settings.base_url, self.db_client)

        invoice._Invoice__is_invalid()

        self.db_client.update.assert_called_once_with(
            filter_query={"id": self.data.id},
            value={"category": CategoriesEnum.INVALID}
        )


if __name__ == '__main__':
    unittest.main()
