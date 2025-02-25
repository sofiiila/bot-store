"""
module invoice look up
"""
import logging

from src.controller.invoice import Invoice
from src.db_client.core import DbClient
from src.db_client.db_client_types import CategoriesEnum, UserDocument

logger = logging.getLogger(__name__)


class InvoiceLookUp:
    """
    Распорядитель заявок для верхнеуровневых ф-й.

    Класс реализует зависимости от БД.

    """
    __invoice_class = Invoice

    def __init__(self, base_url: str, db_client: DbClient, is_overdue_time, tmp_dir):
        self.__base_url = base_url
        self.db_client = db_client
        self.__is_overdue_time = is_overdue_time
        self.__tmp_dir = tmp_dir

    def _construct_invoice(self, data: UserDocument) -> Invoice:
        """
        Общий метод создания Invoice.

        Args:
            data:

        Returns:

        """
        return self.__invoice_class(data=data,
                                    base_url=self.__base_url,
                                    db_client=self.db_client,
                                    is_overdue_time=self.__is_overdue_time,
                                    tmp_dir=self.__tmp_dir)

    def get_oldest_invoice(self) -> Invoice | None:
        """
        возвращает самую старую заявку из очереди или None
        :return: obj Invoice
        """
        result = self.db_client.list(
            filter_query={"category": CategoriesEnum.QUEUE},
            sort_query={"start_date": 1})
        if result:
            logger.debug("Получена заявка с ID: %s",  result[0].id)
            return self._construct_invoice(result[0])
        return None

    # pylint: disable=redefined-builtin
    def get_invoice_by_id(self, invoice_id: str) -> Invoice | None:
        """
        Возвращает заявку которую пора удалять
        :param invoice_id:
        :return: obj Invoice
        """
        logger.debug("получение заявки по id")
        result: list[UserDocument] = self.db_client.list(
            filter_query={"_id": invoice_id},
        )
        if result:
            return self._construct_invoice(result[0])
        return None

    def get_new_invoice_by_user_id(self, user_id: int) -> Invoice | None:
        """
        Возвращает новую заявку для указанного пользователя.

        Args:
            user_id (int): Идентификатор пользователя.

        Returns:
            Invoice | None
        """
        logger.debug("получение заявки по id")
        result: list[UserDocument] = self.db_client.list(
            filter_query={
                "user_id": user_id,
                "category": CategoriesEnum.NEW
            },
        )
        if result:
            return self._construct_invoice(result[0])
        return None

    def get_all_new_invoices(self) -> list[Invoice]:
        """
        Возвращает все заявки со статусом new.
        Returns: Список новых Invoice.
        """
        results_data: list[UserDocument] = self.db_client.list(
            filter_query={"category": CategoriesEnum.NEW}
        )
        return [self._construct_invoice(data=data) for data in results_data]

    def create(self, user_id) -> Invoice:
        """
        Создание новой заявки.

        Args:
            user_id:

        Returns:

        """
        return self.__invoice_class.create(
            user_id=user_id,
            db_client=self.db_client,
            base_url=self.__base_url,
            is_overdue_time=self.__is_overdue_time,
            tmp_dir=self.__tmp_dir)
