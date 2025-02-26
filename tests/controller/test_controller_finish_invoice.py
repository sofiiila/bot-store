import unittest
from unittest.mock import MagicMock
from src.controller.core import Controller
from src.controller.exc import InvoiceNotExist
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

    def test_good_case_finish_invoice(self):
        """
        Тестирование успешного завершения обработки заявки.
        """
        invoice_id = "12345"
        mock_invoice = MagicMock(spec=Invoice)
        self.mock_invoice_lookup.get_invoice_by_id.return_value = mock_invoice

        self.controller.finish_invoice(invoice_id)

        mock_invoice.finish_invoice.assert_called_once()

    def test_bad_case_finish_invoice(self):
        """
        Тестирование поведения метода при отсутствии заявки.
        """
        invoice_id = "12345"
        self.mock_invoice_lookup.get_invoice_by_id.return_value = None

        with self.assertRaises(InvoiceNotExist):
            self.controller.finish_invoice(invoice_id)


if __name__ == '__main__':
    unittest.main()