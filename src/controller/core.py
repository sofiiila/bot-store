"""
eternity cycke & timer
"""
import logging
import time

from src.controller.exc import InvoiceNotExist
from src.controller.invoice import Invoice
from src.controller.invoice_look_up import InvoiceLookUp
from src.db_client.core import DbClient

logger = logging.getLogger(__name__)


class Controller:
    """
    Высокоуровниевый класс, который взаимодействует
    с инфраструктурой приложения.
    """

    def __init__(
        self,
        db_client: DbClient,
        base_url: str,
        queue_time_sleep: int | float = 1,
        overdue_time_sleep: int | float = 1
    ):
        self.__db_client = db_client
        self.__invoice_look_up = InvoiceLookUp(base_url, db_client)
        self.__queue_time_sleep = queue_time_sleep
        self.__overdue_time_sleep = overdue_time_sleep

    def eternity_cycle_iteration(self) -> None:
        """
        Цикл обрабатывающий заявки из очереди
        :return:
        """
        logger.debug("Запущена очередь.(беск цикл)")
        while True:
            invoice: Invoice = self.__invoice_look_up.get_oldest_invoice()
            if invoice is not None:
                invoice.prepare()
            time.sleep(self.__queue_time_sleep)

    def check_timeout_iteration(self) -> None:
        """
        Проверка всех просроченных недозаполненных заявок.
        """
        logger.debug("Запущен таймаут.")
        while True:
            invoices: list[Invoice] = self.__invoice_look_up.get_all_new_invoices()
            for invoice in invoices:
                if invoice.is_overdue:
                    invoice.push_in_queue()
            time.sleep(self.__overdue_time_sleep)

    def finish_invoice(self, invoice_id: str) -> None:
        """
        Подтверждение завершения обработки заявки.

        Args:
            invoice_id: Id заявки.

        """
        invoice: Invoice | None = self.__invoice_look_up.get_invoice_by_id(invoice_id=invoice_id)
        if invoice:
            invoice.finish_invoice()
        else:
            raise InvoiceNotExist

    def update_document_for_user_id(self, user_id: str, update_fields: dict | None = None) -> Invoice:
        """
        Вернет Invoive по user_id и проапдейдит поле.

        Args:
            user_id: Id пользователя
            update_fields: Поля которые надо проапдейтить.

        Returns: Объект Invoice.

        """
        invoice: Invoice | None = self.__invoice_look_up.get_new_invoice_by_user_id(user_id)
        if not invoice:
            invoice = Invoice.create(user_id=user_id, db_client=self.__db_client)
        if update_fields:
            invoice.update_fields(update_fields)
        return invoice


