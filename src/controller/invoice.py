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

    def __init__(self, data: UserDocument, base_url: str, db_client: DbClient, is_overdue_time):
        self.__api_client = CrmApiClient(base_url)
        self.__data = data
        self.__db_client = db_client
        self.__is_overdue_time = is_overdue_time

    @property
    def invoice_id(self):
        return self.__data.id

    @property
    def is_overdue(self) -> bool:
        """
        Просрочена ли заявка.
        :return: Заявка просрочена?
        """
        return datetime.now() - self.__data.start_date > timedelta(minutes=self.__is_overdue_time)

    @property
    def __filter_query(self) -> dict:
        """
        Query фильтрации
        Returns:
        """
        return {"user_id": self.__data.user_id,
                "id": self.__data.id}

    def push_in_queue(self) -> None:
        """
        Cтавит в очередь.
        :return:
        """
        logger.debug(
            "Заявка %s не была заполнена пользователем до конца. Отправляем в очередь",
            self.__data.id
        )
        self.__db_client.update(filter_query=self.__filter_query,
                                value={"category": CategoriesEnum.QUEUE})

    @classmethod
    def create(cls, db_client, user_id, base_url, is_overdue_time) -> 'Invoice':
        """
        Будет вызываться в момеент когда заполнено в боте.
        :return:
        """
        invoice_data = db_client.create(user_id=user_id)
        return cls(data=invoice_data, base_url=base_url, db_client=db_client,
                   is_overdue_time=is_overdue_time)

    def update_fields(self, fields):
        self.__db_client.update(
            filter_query=self.__filter_query,
            value=fields
        )

    def finish_invoice(self):
        """
        метод удаляющий заявку из очереди, когда она уже попала в CRM
        :return:
        """
        logger.debug("Бот получил уведомление о завершении заполнении заявок.")
        self.__db_client.delete(self.__data.id)

    def prepare(self):
        """
        метод решающий куда оптравится заявка после ответа от сервера
        :return:
        """
        logger.debug("обрабатывается статус ответа")
        try:
            self.__api_client.try_send_invoice(
                invoice_data=self.__data.to_api()
            )
            logger.debug("Заявка успешно отправлена.")
            self.__db_client.update(
                filter_query={"id": self.__data.id},
                value={"category": CategoriesEnum.IN_PROGRESS}
            )
        except ServerProblem:
            return
        except InvalidInvoice:
            self.__db_client.update(
                filter_query={"id": self.__data.id},
                value={"category": CategoriesEnum.INVALID}
            )
