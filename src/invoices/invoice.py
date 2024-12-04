import json
import logging
import time
from datetime import datetime, timedelta

import requests
from requests.exceptions import Timeout, ConnectionError

from src.init_app import db_client
from src.invoices.exc import InvalidInvoice, ServerProblem
from src.services.db_client_types import UserDocument, CategoriesEnum

logger = logging.getLogger(__name__)


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
        try:
            response = requests.post(url, json=invoice_data, headers=headers)
            if str(response.status_code).startswith('4'):
                logger.error("400 код.")
                raise InvalidInvoice
            elif str(response.status_code).startswith('5'):
                logger.error("500 код.")
                raise ServerProblem
            else:
                return response.status_code
        except (ConnectionError, Timeout) as e:
            logger.error("Не удачное подключение по причине: %s", str(e))
            raise ServerProblem

    # TODO зачем?
    def get_crm_status(self):
        """
        Метод, который запрашивает статус заявки у CRM
        """
        # url = f"{self.base_url}/api/notifications"
        # headers = {"Content-Type": "application/json"}
        # try:
        #     response = requests.get(url, headers=headers)
        #     if response.status_code == 200:
        #         notification = response.json()
        #         if notification.get("status") == 'ready':
        #             return 'ready'
        #     logger.warning("Уведомление от CRM не содержит ожидаемый статус 'ready'. Код ответа: %d", response.status_code)
        #     return ''
        # except (ConnectionError, Timeout) as e:
        #     logger.error("Не удачное подключение по причине: %s", str(e))
        #     raise ServerProblem
        return 'ready'


class Invoice:
    """
    Класс для работы с заявками, определяет их статус и id
    """

    def __init__(self, data: UserDocument):
        # TODO Base Url должен пробрасывватся черех env
        self.__api_client = CrmApiClient(base_url="http://192.168.0.107:8001")
        self.__data = data

    # TODO реализовать метод
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
        db_client.update(
            filter_query={"id": self.__data.id},
            # TODO Изпользуй enum
            value={"category": "in_progress"}
        )
        self.get_ready_from_crm()

    def is_overdue(self):
        current_time = datetime.now()
        start_date = self.__data.start_date
        delta_time = current_time - start_date
        return delta_time > timedelta(minutes=1)

    def in_queue(self):
        db_client.update(filter_query={"user_id": self.__data.user_id,
                                       "id": self.__data.id},
                         value={"category": CategoriesEnum.queue})

    # TODO Реализовать create
    @classmethod

    def create(cls):
        """
        будет вызываться в момеент когда заполнено в боте
        :return:
        """
        logger.debug("метод create")

    # TODO Убрать
    def get_ready_from_crm(self):
        while True:
            status = self.__api_client.get_crm_status()
            if status == 'ready':
                self.delete()
                break
            time.sleep(10)



    def delete(self):
        """
        метод удаляющий заявку из очереди, когда она уже попала в CRM
        :return:
        """
        logger.debug("Я удаляю ")
        db_client.delete(self.__data.id)

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
