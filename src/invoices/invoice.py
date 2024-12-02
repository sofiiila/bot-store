import json
import logging
from datetime import datetime

import requests

from src.services.db_client_types import UserDocument

logger = logging.getLogger(__name__)


#TODO после подключения сюда db_cmlient :
# добавить методы create() fill() _finish(delay: int,float | None)
class CrmApiClient:
    """
    Клиент для отправки запросов к CRM
    """

    def __init__(self, base_url):
        self.base_url = base_url

    def try_send_invoice(self, invoice_data) -> int:
        url = f"{self.base_url}/api/invoices"
        json_str = json.dumps(invoice_data, default=lambda o: o.isoformat() if isinstance(o, datetime) else o)
        invoice_data = json.loads(json_str)
        headers = {"Content-Type": "application/json"}
        logger.debug('%s %s %s', url, invoice_data, headers)
        response = requests.post(url, json=invoice_data, headers=headers)

        return response.status_code



class Invoice:
    """
    Класс для работы с заявками, определяет их статус и id
    """

    def __init__(self, data: UserDocument):
        self.__api_client = CrmApiClient(base_url="http://localhost:8000")
        self.__data = data

    def __is_invalid(self):
        """
        метод для заявок котрые получили 422 код ответа
        :return:
        """
        logger.debug("инвалид здесб")
        pass

    def __in_progress(self):
        """
        метод дающий заявке статус в процессе, она ждет когда CRM пришлет ready
        :return:
        """
        logger.debug("Вызван ин прогрес")
        pass

    @classmethod
    def create(cls):
        """
        будет вызываться в момеент когда заполнено в боте
        :return:
        """
        logger.debug("метод create")

    def delete(self):
        """
        метод удаляющий заявку из очереди, когда она уже попала в CRM
        :return:
        """
        logger.debug("Я удаляю ")
        pass

    def prepare(self):
        """
        метод решающий куда оптравится заявка после ответа от сервера
        :return:
        """
        logger.debug("обрабатывается статус ответа")
        result = self.__api_client.try_send_invoice(invoice_data=self.__data.to_api())
        logger.debug(f"Код ответа: {result}")
        match result:
            case 200:
                self.__in_progress()
            case 422:
                self.__is_invalid()
