"""
module invoice
"""
import logging

from datetime import datetime, timedelta

from src.controller.client import CrmApiClient
from src.controller.exc import InvalidInvoice, ServerProblem
from src.db_client.core import DbClient
from src.db_client.db_client_types import UserDocument, CategoriesEnum

logger = logging.getLogger(__name__)


class Invoice:  # pylint: disable=too-few-public-methods
    """
    Класс для работы с заявками, определяет их статус и id
    """

    def __init__(self, data: UserDocument, base_url: str, db_client: DbClient):
        self.__api_client = CrmApiClient(base_url)
        self.__data = data
        self.db_client = db_client

    @property
    def is_overdue(self) -> bool:
        """
        Просрочена ли заявка.
        :return: Заявка просрочена?
        """
        return datetime.now() - self.__data.start_date > timedelta(minutes=30)

    @property
    def filter_query(self):
        return {"user_id": self.__data.user_id,
                "id": self.__data.id}

    def push_in_queue(self) -> None:
        """
        Cтавит в очередь.
        :return:
        """
        self.db_client.update(filter_query=self.filter_query,
                              value={"category": CategoriesEnum.QUEUE})

    @classmethod
    def create(cls, db_client, user_id):
        """
        будет вызываться в момеент когда заполнено в боте
        :return:
        """
        return db_client.create(user_id=user_id)

    def update_fields(self, fields):
        self.db_client.update(
            filter_query=self.filter_query,
            value=fields
        )

    def finish_invoice(self):
        """
        метод удаляющий заявку из очереди, когда она уже попала в CRM
        :return:
        """
        logger.debug("Бот получил уведомление о завершении заполнении заявок.")
        self.db_client.delete(self.__data.id)

    def prepare(self):
        """
        метод решающий куда оптравится заявка после ответа от сервера
        :return:
        """
        logger.debug("обрабатывается статус ответа")
        try:
            self.__api_client.try_send_invoice(invoice_data=self.__data.to_api())
            logger.debug("Заявка успешно отправлена.")
            self.db_client.update(
                filter_query={"id": self.__data.id},
                value={"category": CategoriesEnum.IN_PROGRESS}
            )
        except ServerProblem:
            return
        except InvalidInvoice:
            self.db_client.update(
                filter_query={"id": self.__data.id},
                value={"category": CategoriesEnum.INVALID}
            )
