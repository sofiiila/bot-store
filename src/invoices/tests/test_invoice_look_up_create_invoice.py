# import unittest
# from unittest.mock import patch, MagicMock

# from src.invoices.invoice_look_up import InvoiceLookUp


# class TestInvoiceLookUp(unittest.TestCase):
#     def setUp(self):
#         self.base_url = "http://example.com"
#         self.db_client = MagicMock()
#         self.invoice_look_up = InvoiceLookUp(self.base_url, self.db_client)

#     @patch('src.invoices.invoice.Invoice')
#     def test_good_case_create_invoice(self, MockInvoice):
#         data = {"item": "test_item", "quantity": 1}
#         mock_invoice_instance = MockInvoice.return_value

#         result = self.invoice_look_up._InvoiceLookUp__create_invoice(data)

#         MockInvoice.assert_called_once_with(data,
#                                             base_url=self.base_url,
#                                             db_client=self.db_client)

#         self.assertEqual(result, mock_invoice_instance)


# if __name__ == '__main__':
#     unittest.main()
