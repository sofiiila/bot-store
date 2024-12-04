import logging
import threading
import time

from src.init_app import db_client
from src.invoices.invoice import Invoice
from src.services.db_client_types import CategoriesEnum
from src.settings import settings

InvoiceType = Invoice | None

logger = logging.getLogger(__name__)


class InvoiceLookUp:
    """
    Распорядитель заявок для верхнеуровневых ф-й
    """
    def get_oldest_invoice(self) -> InvoiceType:
        """
        возвращает самую старую заявку из очереди или None
        :return: obj Invoice
        """
        result = db_client.list(
            filter_query={"category": CategoriesEnum.queue},
            sort_query={"start_date": 1})
        if result:
            logger.debug("Получена заявка с ID: %s",  result[0].id)
            return Invoice(data=result[0], settings=settings)
        return None

    def get_invoice_by_id(self, id) -> Invoice | None:
        """
        Возвращает заявку которую пора удалять
        :param id:
        :return: obj Invoice
        """
        logger.debug("получение заявки по id")
        result = db_client.list(
            filter_query={"_id": id},
        )
        if result:
            return Invoice(data=result[0], settings=settings)
        return None

    def get_all_new_invoices(self):
        results = db_client.list(
            filter_query={"category": CategoriesEnum.new})
        new_invoices=[]

        if results:
            for result in results:
                new_invoices.append(Invoice(data=result, settings=settings))

        return new_invoices


def eternity_cycle():
    """
    Цикл обрабатывающий заявки из очереди
    :return:
    """
    logger.debug("Запущена очередь.(беск цикл)")
    while True:
        invoice: InvoiceType = InvoiceLookUp().get_oldest_invoice()
        if invoice is not None:
            invoice.prepare()
        time.sleep(1)


def check_timeout():
    logger.debug("Запущен таймаут.")
    while True:
        invoices: list[Invoice] = InvoiceLookUp().get_all_new_invoices()
        for invoice in invoices:
            if invoice.is_overdue() is True:
                invoice.in_queue()
        # TODO время на заполнение заявки тоже должно пробрасываться из env
        time.sleep(1)


def main():
    logging.basicConfig(level=logging.DEBUG)
    thread = threading.Thread(target=eternity_cycle())
    thread.start()


if __name__ == "__main__":
    main()
