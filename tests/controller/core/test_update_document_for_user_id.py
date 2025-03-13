import unittest
from unittest.mock import MagicMock, patch
from src.controller.core import Controller
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

    def test_good_case_update_document_for_user_id_existing_invoice(self):
        """
        Проверяю, что если инвойс найден, то он обновляется.
        """
        user_id = 1
        update_fields = {"field": "value"}
        mock_invoice = MagicMock(spec=Invoice)
        self.mock_invoice_look_up.get_new_invoice_by_user_id.return_value = mock_invoice

        with patch.object(self.controller,
                          '_Controller__invoice_look_up',
                          self.mock_invoice_look_up):
            result = self.controller.update_document_for_user_id(user_id, update_fields)

        mock_invoice.update_fields.assert_called_once_with(update_fields)
        self.assertEqual(result, mock_invoice)

    def test_good_case_update_document_for_user_id_create_invoice(self):
        """
        Проверяю, что если инвойс не найден, то создается новый и обновляется.
        """
        user_id = 1
        update_fields = {"field": "value"}
        mock_invoice = MagicMock(spec=Invoice)
        self.mock_invoice_look_up.get_new_invoice_by_user_id.return_value = None
        self.mock_invoice_look_up.create.return_value = mock_invoice

        with patch.object(self.controller,
                          '_Controller__invoice_look_up',
                          self.mock_invoice_look_up):
            result = self.controller.update_document_for_user_id(user_id, update_fields)

        mock_invoice.update_fields.assert_called_once_with(update_fields)
        self.assertEqual(result, mock_invoice)

    def test_bad_case_update_document_for_user_id_existing_invoice(self):
        """
        Проверяю, что если инвойс найден, но обновление не выполняется.
        """
        user_id = 1
        update_fields = {"field": "value"}
        mock_invoice = MagicMock(spec=Invoice)
        mock_invoice.update_fields.side_effect = Exception("Обновление не выполнено")
        self.mock_invoice_look_up.get_new_invoice_by_user_id.return_value = mock_invoice

        with patch.object(self.controller,
                          '_Controller__invoice_look_up',
                          self.mock_invoice_look_up):
            with self.assertRaises(Exception):
                self.controller.update_document_for_user_id(user_id, update_fields)

    # TODO тут по сути проверка одного и того-же, один убери на выбор. А вместо этого проверь два кейса когда выбрасываются в эксепшены в методах лукапа.
    def test_bad_case_update_document_for_user_id_create_invoice(self):
        """
        Проверяю, что если инвойс создается, но обновление не выполняется.
        """
        user_id = 1
        update_fields = {"field": "value"}
        mock_invoice = MagicMock(spec=Invoice)
        mock_invoice.update_fields.side_effect = Exception("Обновление не выполнено")
        self.mock_invoice_look_up.get_new_invoice_by_user_id.return_value = None
        self.mock_invoice_look_up.create.return_value = mock_invoice

        with patch.object(self.controller,
                          '_Controller__invoice_look_up',
                          self.mock_invoice_look_up):
            with self.assertRaises(Exception):
                self.controller.update_document_for_user_id(user_id, update_fields)

    #TODO А это кстати бага, надо в функции будет добавить выброс исключения если не один не вернул. 
    # И тут протестировать что будет выбран этот exception.
    
    def test_bad_case_update_document_for_user_id_both_is_none(self):
        """
        Проверяю, что если оба метода возвращают None, то update_fields не вызывается.
        """
        self.mock_invoice_look_up.get_new_invoice_by_user_id.return_value = None
        self.mock_invoice_look_up.create.return_value = None

        mock_invoice = MagicMock(spec=Invoice)

        with patch.object(self.controller,
                          '_Controller__invoice_look_up',
                          self.mock_invoice_look_up):
            mock_invoice.update_fields.assert_not_called()


if __name__ == '__main__':
    unittest.main()
