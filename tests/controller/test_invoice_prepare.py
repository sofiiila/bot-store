import unittest
from unittest.mock import MagicMock, patch
from src.controller.invoice import Invoice, UserDocument, DbClient, ServerProblem, InvalidInvoice, CategoriesEnum


class TestInvoice(unittest.TestCase):
    def setUp(self):
        self.data = MagicMock(spec=UserDocument)
        self.data.id = 123
        self.data.to_api.return_value = {"id": 123, "amount": 100.0}
        self.base_url = "http://example.com"
        self.is_overdue_time = False
        self.tmp_dir = "/tmp"
        self.db_client = MagicMock(spec=DbClient)

    @patch('src.controller.invoice.CrmApiClient')
    def test_good_case_prepare(self, MockCrmApiClient):
        """
        Тестирует успешное выполнение метода prepare
        """
        invoice = Invoice(
            data=self.data,
            base_url=self.base_url,
            db_client=self.db_client,
            is_overdue_time=self.is_overdue_time,
            tmp_dir=self.tmp_dir
        )
        invoice._Invoice__api_client = MockCrmApiClient.return_value

        invoice.prepare()

        invoice._Invoice__api_client.try_send_invoice.assert_called_once_with(invoice_data=self.data.to_api())
        self.db_client.update.assert_called_once_with(
            filter_query={"id": self.data.id},
            value={"category": CategoriesEnum.IN_PROGRESS}
        )

    @patch('src.controller.invoice.CrmApiClient')
    def test_bad_case_prepare_server_problem(self, MockCrmApiClient):
        """
        Тестирует случай, когда возникает ошибка ServerProblem
        """
        invoice = Invoice(
            data=self.data,
            base_url=self.base_url,
            db_client=self.db_client,
            is_overdue_time=self.is_overdue_time,
            tmp_dir=self.tmp_dir
        )
        invoice._Invoice__api_client = MockCrmApiClient.return_value
        invoice._Invoice__api_client.try_send_invoice.side_effect = ServerProblem

        result = invoice.prepare()

        invoice._Invoice__api_client.try_send_invoice.assert_called_once_with(invoice_data=self.data.to_api())
        self.assertIsNone(result)
        self.db_client.update.assert_not_called()

    @patch('src.controller.invoice.CrmApiClient')
    def test_bad_case_prepare_invalid_invoice(self, MockCrmApiClient):
        """
        Тестирует случай, когда возникает ошибка InvalidInvoice
        """
        invoice = Invoice(
            data=self.data,
            base_url=self.base_url,
            db_client=self.db_client,
            is_overdue_time=self.is_overdue_time,
            tmp_dir=self.tmp_dir
        )
        invoice._Invoice__api_client = MockCrmApiClient.return_value
        invoice._Invoice__api_client.try_send_invoice.side_effect = InvalidInvoice

        invoice.prepare()

        invoice._Invoice__api_client.try_send_invoice.assert_called_once_with(invoice_data=self.data.to_api())
        self.db_client.update.assert_called_once_with(
            filter_query={"id": self.data.id},
            value={"category": CategoriesEnum.INVALID}
        )


if __name__ == '__main__':
    unittest.main()