import unittest
from unittest.mock import MagicMock, patch
from src.controller.invoice import Invoice, UserDocument, DbClient


class TestInvoice(unittest.TestCase):
    def setUp(self):
        self.data = MagicMock(spec=UserDocument)
        self.data.id = 123
        self.data.user_id = 1
        self.base_url = "http://example.com"
        self.is_overdue_time = False
        self.tmp_dir = "/tmp"
        self.db_client = MagicMock(spec=DbClient)

    @patch('src.controller.invoice.CrmApiClient')
    def test_good_case_update_fields(self, MockCrmApiClient):
        """
        Тестирует успешное обновление полей заявки
        """
        invoice = Invoice(
            data=self.data,
            base_url=self.base_url,
            db_client=self.db_client,
            is_overdue_time=self.is_overdue_time,
            tmp_dir=self.tmp_dir
        )

        fields_to_update = {"status": "обновлено"}

        invoice.update_fields(fields_to_update)

        self.db_client.update.assert_called_once_with(
            filter_query={"user_id": self.data.user_id, "id": self.data.id},
            value=fields_to_update
        )

    @patch('src.controller.invoice.CrmApiClient')
    def test_bad_case_update_fields(self, MockCrmApiClient):
        """
        Тестирует случай, когда обновление полей заявки не удается
        """
        invoice = Invoice(
            data=self.data,
            base_url=self.base_url,
            db_client=self.db_client,
            is_overdue_time=self.is_overdue_time,
            tmp_dir=self.tmp_dir
        )

        fields_to_update = {"status": "approved"}

        self.db_client.update.side_effect = Exception("Не обновилось")

        with self.assertRaises(Exception):
            invoice.update_fields(fields_to_update)


if __name__ == '__main__':
    unittest.main()
