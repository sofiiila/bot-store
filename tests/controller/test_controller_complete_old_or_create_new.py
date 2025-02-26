import unittest
from unittest.mock import MagicMock, patch
from src.controller.core import Controller
from src.controller.invoice import Invoice


class TestController(unittest.TestCase):
    def setUp(self):
        self.db_client = MagicMock()
        self.base_url = "http://example.com"
        self.is_overdue_time = 0
        self.queue_time_sleep = 1
        self.overdue_time_sleep = 1
        self.tmp_dir = "/tmp"
        self.controller = Controller(
            db_client=self.db_client,
            base_url=self.base_url,
            is_overdue_time=self.is_overdue_time,
            queue_time_sleep=self.queue_time_sleep,
            overdue_time_sleep=self.overdue_time_sleep,
            tmp_dir=self.tmp_dir
        )

        self.mock_invoice_lookup = MagicMock()
        self.controller._Controller__invoice_look_up = self.mock_invoice_lookup

    def test_good_case_update_document_for_user_id(self):
        """
        успешноe обновлениe документа для пользователя.
        """
        user_id = 123
        update_fields = {"status": "updated"}
        mock_invoice = MagicMock(spec=Invoice)
        self.mock_invoice_lookup.get_new_invoice_by_user_id.return_value = mock_invoice

        result = self.controller.update_document_for_user_id(user_id, update_fields)

        mock_invoice.update_fields.assert_called_once_with(update_fields)
        self.assertEqual(result, mock_invoice)

    def test_bad_case_update_document_for_user_id(self):
        """
        неудачноe обновлениe документа для пользователя.
        """
        user_id = 123
        self.mock_invoice_lookup.get_new_invoice_by_user_id.return_value = None
        self.mock_invoice_lookup.create.side_effect = Exception("Failed to create invoice")

        with self.assertRaises(Exception):
            self.controller.update_document_for_user_id(user_id)


if __name__ == '__main__':
    unittest.main()