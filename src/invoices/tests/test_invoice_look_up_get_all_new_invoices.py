import unittest
from unittest.mock import MagicMock
from src.invoices.invoice import Invoice
from src.invoices.invoice_look_up import InvoiceLookUp
from src.services.db_client_types import CategoriesEnum


class TestInvoiceLookUp(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://example.com"
        self.db_client = MagicMock()
        self.invoice_lookup = InvoiceLookUp(self.base_url, self.db_client)

    def test_good_case_get_all_new_invoices(self):
        mock_invoice_data_1 = MagicMock()
        mock_invoice_data_2 = MagicMock()
        self.db_client.list.return_value = [mock_invoice_data_1, mock_invoice_data_2]

        result = self.invoice_lookup.get_all_new_invoices()

        self.assertEqual(len(result), 2)
        self.db_client.list.assert_called_once_with(
            filter_query={"category": CategoriesEnum.NEW}
        )
        self.assertIsInstance(result[0], Invoice)
        self.assertIsInstance(result[1], Invoice)

    def test_bad_case_get_all_new_invoices(self):
        self.db_client.list.return_value = []

        result = self.invoice_lookup.get_all_new_invoices()

        self.assertEqual(len(result), 0)
        self.db_client.list.assert_called_once_with(
            filter_query={"category": CategoriesEnum.NEW}
        )


if __name__ == '__main__':
    unittest.main()
