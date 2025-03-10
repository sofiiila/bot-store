import unittest
from unittest.mock import MagicMock, patch
from src.controller.invoice import Invoice, UserDocument, DbClient


class TestInvoice(unittest.TestCase):
    def setUp(self):
        self.data = MagicMock(spec=UserDocument)
        self.data.id = 123
        self.base_url = "http://example.com"
        self.is_overdue_time = False
        self.tmp_dir = "/tmp"
        self.db_client = MagicMock(spec=DbClient)

    @patch('src.controller.invoice.CrmApiClient')
    def test_good_case_finish_invoice(self, _):
        """
        успешное удаление заявки из очереди
        """
        invoice = Invoice(
            data=self.data,
            base_url=self.base_url,
            db_client=self.db_client,
            is_overdue_time=self.is_overdue_time,
            tmp_dir=self.tmp_dir
        )

        invoice.finish_invoice()

        self.db_client.delete.assert_called_once_with(self.data.id)

    @patch('src.controller.invoice.CrmApiClient')
    def test_bad_case_finish_invoice(self, _):
        """
        Удаление заявки из очереди не удается
        """
        invoice = Invoice(
            data=self.data,
            base_url=self.base_url,
            db_client=self.db_client,
            is_overdue_time=self.is_overdue_time,
            tmp_dir=self.tmp_dir
        )

        self.db_client.delete.side_effect = Exception("Не удалось удалить заявку")

        with self.assertRaises(Exception):
            invoice.finish_invoice()

        self.db_client.delete.assert_called_once_with(self.data.id)


if __name__ == '__main__':
    unittest.main()
