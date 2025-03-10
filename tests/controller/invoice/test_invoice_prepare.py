import unittest
from unittest.mock import MagicMock, patch
from src.controller.invoice import Invoice, UserDocument, DbClient, \
      ServerProblem, InvalidInvoice, CategoriesEnum


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
    def test_good_case_prepare(self, mock_crm_api_client):
        """
        Успешная отправка и обновление
        """
        mock_api_client = mock_crm_api_client.return_value
        invoice = Invoice(
            data=self.data,
            base_url=self.base_url,
            db_client=self.db_client,
            is_overdue_time=self.is_overdue_time,
            tmp_dir=self.tmp_dir
        )

        invoice.prepare()

        mock_api_client.try_send_invoice.assert_called_once_with(invoice_data=self.data.to_api())
        self.db_client.update.assert_called_once_with(
            filter_query={"id": self.data.id},
            value={"category": CategoriesEnum.IN_PROGRESS}
        )

    @patch('src.controller.invoice.CrmApiClient')
    def test_good_case_prepare_server_problem(self, mock_crm_api_client):
        """
        Исключение ServerProblem
        """
        mock_api_client = mock_crm_api_client.return_value
        mock_api_client.try_send_invoice.side_effect = ServerProblem
        invoice = Invoice(
            data=self.data,
            base_url=self.base_url,
            db_client=self.db_client,
            is_overdue_time=self.is_overdue_time,
            tmp_dir=self.tmp_dir
        )

        invoice.prepare()

        mock_api_client.try_send_invoice.assert_called_once_with(invoice_data=self.data.to_api())
        self.db_client.update.assert_not_called()

    @patch('src.controller.invoice.CrmApiClient')
    def test_good_case_prepare_invalid_invoice(self, mock_crm_api_client):
        """
        Исключение InvalidInvoice и успешное обновление категории на инвалид
        """
        mock_api_client = mock_crm_api_client.return_value
        mock_api_client.try_send_invoice.side_effect = InvalidInvoice
        invoice = Invoice(
            data=self.data,
            base_url=self.base_url,
            db_client=self.db_client,
            is_overdue_time=self.is_overdue_time,
            tmp_dir=self.tmp_dir
        )

        invoice.prepare()

        mock_api_client.try_send_invoice.assert_called_once_with(invoice_data=self.data.to_api())
        self.db_client.update.assert_called_once_with(
            filter_query={"id": self.data.id},
            value={"category": CategoriesEnum.INVALID}
        )

    @patch('src.controller.invoice.CrmApiClient')
    def test_bad_case_prepare_invalid_invoice(self, mock_crm_api_client):
        """
        Исключение InvalidInvoice и неудачное обновление
        """
        mock_api_client = mock_crm_api_client.return_value
        mock_api_client.try_send_invoice.side_effect = InvalidInvoice
        self.db_client.update.side_effect = Exception("Обновление не удалось")
        invoice = Invoice(
            data=self.data,
            base_url=self.base_url,
            db_client=self.db_client,
            is_overdue_time=self.is_overdue_time,
            tmp_dir=self.tmp_dir
        )

        with self.assertRaises(Exception):
            invoice.prepare()

        mock_api_client.try_send_invoice.assert_called_once_with(invoice_data=self.data.to_api())
        self.db_client.update.assert_called_once_with(
            filter_query={"id": self.data.id},
            value={"category": CategoriesEnum.INVALID}
        )

    @patch('src.controller.invoice.CrmApiClient')
    def test_bad_case_prepare_other_exception(self, mock_crm_api_client):
        """
        Другое исключение
        """
        mock_api_client = mock_crm_api_client.return_value
        mock_api_client.try_send_invoice.side_effect = Exception("Неизвестная ошибка")
        invoice = Invoice(
            data=self.data,
            base_url=self.base_url,
            db_client=self.db_client,
            is_overdue_time=self.is_overdue_time,
            tmp_dir=self.tmp_dir
        )

        with self.assertRaises(Exception):
            invoice.prepare()

        mock_api_client.try_send_invoice.assert_called_once_with(invoice_data=self.data.to_api())
        self.db_client.update.assert_not_called()

    @patch('src.controller.invoice.CrmApiClient')
    def test_bad_case_prepare_send_success_update_fails(self, mock_crm_api_client):
        """
        Успешная отправка, но обновление не удается
        """
        mock_api_client = mock_crm_api_client.return_value
        self.db_client.update.side_effect = Exception("Обновление не удалось")
        invoice = Invoice(
            data=self.data,
            base_url=self.base_url,
            db_client=self.db_client,
            is_overdue_time=self.is_overdue_time,
            tmp_dir=self.tmp_dir
        )

        with self.assertRaises(Exception):
            invoice.prepare()

        mock_api_client.try_send_invoice.assert_called_once_with(invoice_data=self.data.to_api())
        self.db_client.update.assert_called_once_with(
            filter_query={"id": self.data.id},
            value={"category": CategoriesEnum.IN_PROGRESS}
        )


if __name__ == '__main__':
    unittest.main()
