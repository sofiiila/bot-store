import unittest
from unittest.mock import patch, MagicMock

from datetime import datetime
from requests.exceptions import ConnectionError, Timeout

from src.controller.exc import InvalidInvoice, ServerProblem
from src.controller.invoice import CrmApiClient


class TestCrmApiClient(unittest.TestCase):

    def setUp(self):
        self.base_url = "http://example.com"
        self.client = CrmApiClient(base_url=self.base_url)

    @patch('requests.post')
    def test_good_case_try_send_invoice(self, mock_post):
        """
        Проверяет успешную отправку заявки в CRM
        """
        invoice_data = {
            "id": 1,
            "date": datetime.now().isoformat(),
            "amount": 100.0
        }
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_post.return_value = mock_response

        result = self.client.try_send_invoice(invoice_data)

        mock_post.assert_called_once_with(
            f"{self.base_url}/api/invoices",
            json=invoice_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )
        self.assertEqual(result, 200)

    @patch('requests.post')
    def test_good_case_try_send_invoice_4xx(self, mock_post):
        """
        Проверяет случай, когда ответ имеет статус 4xx
        """
        invoice_data = {
            "id": 1,
            "date": datetime.now().isoformat(),
            "amount": 100.0
        }
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_post.return_value = mock_response

        with self.assertRaises(InvalidInvoice):
            self.client.try_send_invoice(invoice_data)

        mock_post.assert_called_once_with(
            f"{self.base_url}/api/invoices",
            json=invoice_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )

    @patch('requests.post')
    def test_good_case_try_send_invoice_5xx(self, mock_post):
        """
        Проверяет случай, когда ответ имеет статус 5xx
        """
        invoice_data = {
            "id": 1,
            "date": datetime.now().isoformat(),
            "amount": 100.0
        }
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_post.return_value = mock_response

        with self.assertRaises(ServerProblem):
            self.client.try_send_invoice(invoice_data)

        mock_post.assert_called_once_with(
            f"{self.base_url}/api/invoices",
            json=invoice_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )

    @patch('requests.post')
    def test_bad_case_try_send_invoice_connection_error(self, mock_post):
        """
        Проверяет случай, когда возникает ошибка подключения
        """
        invoice_data = {
            "id": 1,
            "date": datetime.now().isoformat(),
            "amount": 100.0
        }
        mock_post.side_effect = ConnectionError("Connection error")

        with self.assertRaises(ServerProblem):
            self.client.try_send_invoice(invoice_data)

        mock_post.assert_called_once_with(
            f"{self.base_url}/api/invoices",
            json=invoice_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )

    @patch('requests.post')
    def test_bad_case_try_send_invoice_timeout(self, mock_post):
        """
        Проверяет случай, когда возникает тайм-аут
        """
        invoice_data = {
            "id": 1,
            "date": datetime.now().isoformat(),
            "amount": 100.0
        }
        mock_post.side_effect = Timeout("Timeout error")

        with self.assertRaises(ServerProblem):
            self.client.try_send_invoice(invoice_data)

        mock_post.assert_called_once_with(
            f"{self.base_url}/api/invoices",
            json=invoice_data,
            headers={"Content-Type": "application/json"},
            timeout=10
        )


if __name__ == '__main__':
    unittest.main()
