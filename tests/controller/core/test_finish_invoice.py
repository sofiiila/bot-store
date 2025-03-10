import unittest
from unittest.mock import MagicMock
from src.controller.core import Controller
from src.controller.exc import InvoiceNotExist
from src.controller.invoice import Invoice
from src.controller.invoice_look_up import InvoiceLookUp


class TestController(unittest.TestCase):

    def setUp(self):
        self.db_client = MagicMock()
        self.base_url = "http://example.com"
        self.is_overdue_time = 10
        self.mock_invoice_look_up = MagicMock(spec=InvoiceLookUp)
        self.controller = Controller(
            db_client=self.db_client,
            base_url=self.base_url,
            is_overdue_time=self.is_overdue_time
        )
        self.controller.get_invoice_look_up = MagicMock(return_value=self.mock_invoice_look_up)

    def test_good_case_finish_invoice(self):
        """
        Проверяю, что если инвойс найден, то он завершается.
        """
        invoice_id = "123"
        mock_invoice = MagicMock(spec=Invoice)
        self.mock_invoice_look_up.get_invoice_by_id.return_value = mock_invoice

        self.controller.finish_invoice(invoice_id)

        mock_invoice.finish_invoice.assert_called_once()

    def test_good_case_finish_invoice_is_none(self):
        """
        Проверяю, что если инвойс не найден, выбрасывается исключение.
        """
        invoice_id = "123"
        self.mock_invoice_look_up.get_invoice_by_id.return_value = None

        with self.assertRaises(InvoiceNotExist):
            self.controller.finish_invoice(invoice_id)

    def test_bad_case_finish_invoice_no_finish(self):
        """
        Проверяю, что если инвойс найден, но не завершается.
        """
        invoice_id = "123"
        mock_invoice = MagicMock(spec=Invoice)
        mock_invoice.finish_invoice.side_effect = Exception("Не удалось завершить инвойс")
        self.mock_invoice_look_up.get_invoice_by_id.return_value = mock_invoice

        with self.assertRaises(Exception):
            self.controller.finish_invoice(invoice_id)

        mock_invoice.finish_invoice.assert_called_once()


if __name__ == '__main__':
    unittest.main()
