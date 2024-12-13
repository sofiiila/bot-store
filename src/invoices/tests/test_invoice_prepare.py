import unittest
from unittest.mock import MagicMock, patch
from src.invoices.invoice import Invoice, Settings, UserDocument, ServerProblem, InvalidInvoice


class TestInvoice(unittest.TestCase):
    def setUp(self):
        self.data = MagicMock(spec=UserDocument)
        self.data.id = 123
        self.data.to_api.return_value = {"id": 123, "amount": 100.0}
        self.settings = MagicMock(spec=Settings)
        self.settings.base_url = "http://example.com"
        self.db_client = MagicMock()

    @patch('src.invoices.invoice.CrmApiClient')
    @patch('src.invoices.invoice.Invoice._Invoice__is_invalid')
    @patch('src.invoices.invoice.Invoice._Invoice__in_progress')
    def test_good_case_prepare(self, mock_in_progress, mock_is_invalid, MockCrmApiClient):
        """
        Метод в случае когда отвечает успешно
        """
        invoice = Invoice(self.data, self.settings.base_url, self.db_client)
        invoice._Invoice__api_client = MockCrmApiClient.return_value

        invoice.prepare()

        invoice._Invoice__api_client.try_send_invoice.assert_called_once_with(invoice_data=self.data.to_api())
        mock_in_progress.assert_called_once()

    @patch('src.invoices.invoice.CrmApiClient')
    @patch('src.invoices.invoice.Invoice._Invoice__is_invalid')
    @patch('src.invoices.invoice.Invoice._Invoice__in_progress')
    def test_bad_case_prepare_server_problem(self, mock_in_progress, mock_is_invalid, MockCrmApiClient):
        """
        В случае ошибки ServerProblem
        """
        invoice = Invoice(self.data, self.settings.base_url, self.db_client)
        invoice._Invoice__api_client = MockCrmApiClient.return_value
        invoice._Invoice__api_client.try_send_invoice.side_effect = ServerProblem

        result = invoice.prepare()

        invoice._Invoice__api_client.try_send_invoice.assert_called_once_with(invoice_data=self.data.to_api())
        self.assertIsNone(result)

    @patch('src.invoices.invoice.CrmApiClient')
    @patch('src.invoices.invoice.Invoice._Invoice__is_invalid')
    @patch('src.invoices.invoice.Invoice._Invoice__in_progress')
    def test_bad_case_prepare_invalid_invoice(self, mock_in_progress, mock_is_invalid, MockCrmApiClient):
        """
        В случае ошибки InvalidInvoice
        """
        invoice = Invoice(self.data, self.settings.base_url, self.db_client)
        invoice._Invoice__api_client = MockCrmApiClient.return_value
        invoice._Invoice__api_client.try_send_invoice.side_effect = InvalidInvoice

        invoice.prepare()

        invoice._Invoice__api_client.try_send_invoice.assert_called_once_with(invoice_data=self.data.to_api())
        mock_is_invalid.assert_called_once()


if __name__ == '__main__':
    unittest.main()
