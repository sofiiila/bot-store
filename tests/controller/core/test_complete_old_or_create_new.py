import unittest
from unittest.mock import MagicMock

from src.controller.core import Controller
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
        self.controller._Controller__invoice_look_up = self.mock_invoice_look_up

    def test_good_case_complete_old(self):
        """
        Проверяю что функция работает при наличии  существующей заявки
        и ставится в очередь на обработку
        """
        user_id = 1
        mock_invoice = MagicMock()
        self.mock_invoice_look_up.get_new_invoice_by_user_id.return_value = mock_invoice

        self.controller.complete_old_or_create_new(user_id)

        mock_invoice.push_in_queue.assert_called_once()
        self.mock_invoice_look_up.create.assert_not_called()

    def test_good_case_create_new(self):
        """
        Проверяю что при отсутсвии существующей заявки
        функция создает новую заявку
        """
        user_id = 1
        self.mock_invoice_look_up.get_new_invoice_by_user_id.return_value = None

        self.controller.complete_old_or_create_new(user_id)

        self.mock_invoice_look_up.create.assert_called_once_with(user_id=user_id)

    def test_bad_case_not_complete_old_and_not_create_new_(self):
        """
        Случай когда нет существующего инвойса и не создается новый
        """

        user_id = 1
        self.mock_invoice_look_up.get_new_invoice_by_user_id.return_value = None
        self.mock_invoice_look_up.create.side_effect = Exception("Не создана заявка")

        with self.assertRaises(Exception):
            self.controller.complete_old_or_create_new(user_id)

    def test_bad_case_complete_old_not_push_in_queue(self):
        """
        Случай когда есть существующая заявка, но проблема с очередью
        """
        user_id = 1
        mock_invoice = MagicMock()
        mock_invoice.push_in_queue.side_effect = Exception("Не в очереди")
        self.mock_invoice_look_up.get_new_invoice_by_user_id.return_value = mock_invoice

        with self.assertRaises(Exception):
            self.controller.complete_old_or_create_new(user_id)


if __name__ == '__main__':
    unittest.main()
