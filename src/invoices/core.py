import logging
import threading
import time

from src.init_app import db_client
from src.invoices import invoice
from src.invoices.invoice import Invoice
from src.services.db_client_types import CategoriesEnum, UserDocument

LastInvoiceLookUpType = Invoice | None

logger = logging.getLogger(__name__)


class InvoiceLookUp:
    """
    Распорядитель заявок для верхнеуровневых ф-й
    """
    def get_oldest_invoice(self) -> LastInvoiceLookUpType:
        """
        возвращает самую старую заявку из очереди или None
        :return: obj Invoice
        """
        result = db_client.list(
            filter_query={"category": CategoriesEnum.queue},
            sort_query={"start_date": 1})
        if result:
            logger.debug("Получена заявка с ID: %s",  result[0].id)
            return Invoice(data=result[0])
        return None

    def get_invoice_by_id(self, id) -> LastInvoiceLookUpType | None:
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
            return Invoice(data=result[0])
        return None
    #TODO неправильно тип что возвращается и он должен вернуть объект Ivoice


def eternity_cycle():
    """
    Цикл обрабатывающий заявки из очереди
    :return:
    """
    logger.debug("запуск бесконечного цикла")
    while True:
        invoice: LastInvoiceLookUpType = InvoiceLookUp().get_oldest_invoice()
        if invoice is not None:
            invoice.prepare()
        time.sleep(1)


def main():
    logging.basicConfig(level=logging.DEBUG)
    thread = threading.Thread(target=eternity_cycle())
    thread.start()


if __name__ == "__main__":
    main()
