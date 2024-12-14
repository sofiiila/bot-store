import unittest
from unittest.mock import MagicMock, patch
from src.invoices.invoice import Invoice
from src.services.db_client_types import CategoriesEnum, UserDocument
from src.settings import Settings


class TestInvoice(unittest.TestCase):
    def setUp(self):
        self.data = MagicMock(spec=UserDocument)
        self.data.id = 123
        self.settings = MagicMock(spec=Settings)
        self.settings.base_url = "http://example.com"
        self.db_client = MagicMock()

    @patch('src.invoices.invoice.CrmApiClient')
    def test_good_case_in_progress(self, _):
        """
        Метод __in_progress добавляет категорию in_progress в БД
        """
        invoice = Invoice(self.data, self.settings.base_url, self.db_client)

        invoice.in_progress = True

        self.db_client.update.assert_called_once_with(
            filter_query={"id": self.data.id},
            value={"category": CategoriesEnum.IN_PROGRESS}
        )


if __name__ == '__main__':
    unittest.main()
