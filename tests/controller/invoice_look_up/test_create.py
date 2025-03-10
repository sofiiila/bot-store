import unittest
from unittest.mock import patch, MagicMock
from src.controller.invoice_look_up import InvoiceLookUp


class TestInvoiceLookUp(unittest.TestCase):
    def setUp(self):
        self.base_url = "http://example.com"
        self.is_overdue_time = False
        self.tmp_dir = "/tmp"
        self.db_client = MagicMock()
        self.invoice_look_up = InvoiceLookUp(self.base_url, self.db_client,
                                             self.is_overdue_time, self.tmp_dir)

    @patch('src.controller.invoice.Invoice.create')
    def test_good_case_create(self, mock_create):
        """
        Заявка успешно создается
        """
        user_id = "12345"
        mock_invoice_instance = mock_create.return_value

        result = self.invoice_look_up.create(user_id)

        mock_create.assert_called_once_with(user_id=user_id, db_client=self.db_client,
                                           base_url=self.base_url,
                                           is_overdue_time=self.is_overdue_time,
                                           tmp_dir=self.tmp_dir)

        self.assertEqual(result, mock_invoice_instance)

    @patch('src.controller.invoice.Invoice.create')
    def test_bad_case_create(self, mock_create):
        """
        Заявка не создается из-за ошибки
        """
        user_id = "12345"
        mock_create.side_effect = Exception("Не удалось создать Invoice")

        with self.assertRaises(Exception):
            self.invoice_look_up.create(user_id)

        mock_create.assert_called_once_with(user_id=user_id, db_client=self.db_client,
                                           base_url=self.base_url,
                                           is_overdue_time=self.is_overdue_time,
                                           tmp_dir=self.tmp_dir)


if __name__ == '__main__':
    unittest.main()
