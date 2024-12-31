import json
import logging
from datetime import datetime

import requests
from requests import Timeout

from src.controller.exc import InvalidInvoice, ServerProblem

logger = logging.getLogger(__name__)


class CrmApiClient:  # pylint: disable=too-few-public-methods
    """
    Клиент для отправки запросов к CRM
    """

    def __init__(self, base_url):
        self.base_url = base_url

    def try_send_invoice(self, invoice_data) -> int:
        """
        Ф-я пытающаяся отправить заявку в CRM
        :param invoice_data:
        :return:
        """
        url = f"{self.base_url}/api/invoices"
        json_str = json.dumps(invoice_data,
                              default=lambda o: o.isoformat() if isinstance(o, datetime) else o)
        invoice_data = json.loads(json_str)
        headers = {"Content-Type": "application/json"}
        logger.debug('%s %s %s', url, invoice_data, headers)
        try:
            response = requests.post(url, json=invoice_data, headers=headers, timeout=10)
            if str(response.status_code).startswith('4'):
                logger.error("400 код.")
                raise InvalidInvoice
            if str(response.status_code).startswith('5'):
                logger.error("500 код.")
                raise ServerProblem

            return response.status_code
        except (ConnectionError, Timeout) as e:
            logger.error("Неудачное подключение по причине: %s", str(e))
            raise ServerProblem from e
