"""
module invoice
"""
import json
import logging

from datetime import datetime, timedelta

import requests
from requests.exceptions import Timeout

from src.invoices.exc import InvalidInvoice, ServerProblem
from src.services.db_client_types import UserDocument, CategoriesEnum
from src.settings import Settings

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


class Invoice:  # pylint: disable=too-few-public-methods
    """
    Класс для работы с заявками, определяет их статус и id
    """

    def __init__(self, data: UserDocument, base_url, db_client):
        # TODO Base Url должен пробрасывватся черех env
        self.__api_client = CrmApiClient(base_url)
        self.__data = data
        self.db_client = db_client

    def __is_invalid(self):
        """
        метод для заявок котрые получили 422 код ответа
        :return:
        """
        logger.debug("инвалид здесб")
        self.db_client.update(
            filter_query={"id": self.__data.id},
            value={"category": CategoriesEnum.INVALID}
        )

    @property
    def is_invalid(self):
        return self.__is_invalid

    @is_invalid.setter
    def is_invalid(self, value):
        if value:
            self.db_client.update(CategoriesEnum.INVALID)

    def __in_progress(self):
        """
        метод дающий заявке статус в процессе, она ждет когда CRM пришлет ready
        :return:
        """
        logger.debug("Вызван ин прогрес")
        self.db_client.update(
            filter_query={"id": self.__data.id},
            # TODO Изпользуй enum
            value={"category": CategoriesEnum.IN_PROGRESS}
        )

    @property
    def in_progress(self):
        """Свойство для проверки статуса заявки."""
        return self.__data.category == CategoriesEnum.IN_PROGRESS

    @in_progress.setter
    def in_progress(self, value):
        if value:
            self.__in_progress()

    def is_overdue(self):
        """
        timer для заполнения
        :return:
        """
        current_time = datetime.now()
        start_date = self.__data.start_date
        delta_time = current_time - start_date
        return delta_time > timedelta(minutes=30)

    def in_queue(self):
        """
        ставит в queue
        :return:
        """
        self.db_client.update(filter_query={"user_id": self.__data.user_id,
                              "id": self.__data.id},
                              value={"category": CategoriesEnum.QUEUE})

    # TODO Реализовать create
    @classmethod
    def create(cls, data: UserDocument, settings: Settings, db_client):
        """
        будет вызываться в момеент когда заполнено в боте
        :return:
        """
        logger.debug("метод create")
        invoice = cls(data, settings, db_client)
        invoice.in_queue()
        return invoice

    def delete(self):
        """
        метод удаляющий заявку из очереди, когда она уже попала в CRM
        :return:
        """
        logger.debug("Я удаляю ")
        self.db_client.delete(self.__data.id)

    def prepare(self):
        """
        метод решающий куда оптравится заявка после ответа от сервера
        :return:
        """
        logger.debug("обрабатывается статус ответа")
        try:
            self.__api_client.try_send_invoice(invoice_data=self.__data.to_api())
        except ServerProblem:
            return
        except InvalidInvoice:
            self.__is_invalid()
        self.__in_progress()

    @property
    def api_client(self):
        return self.__api_client

    @api_client.setter
    def api_client(self, value):
        self.__api_client = value
