import logging
import threading
import time

from src.bot_types import InvoiceDataType
from src.init_app import db_client
from src.invoices.invoice import Invoice
from src.services.core import DbClient
from src.services.db_client_types import CategoriesEnum

LastInvoiceLookUpType = InvoiceDataType | None

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
        logger.debug("Функуия определяющая последнюю заявку")
        result = db_client.list(
            filter_query={"category": CategoriesEnum.queue},
            sort_querty={"create_time": -1})
        if result:
            return result[0]
        return None

    def get_invoice_by_id(self, id) -> LastInvoiceLookUpType:
        """
        Возвращает заявку которую пора удалять
        :param id:
        :return: obj Invoice
        """
        logger.debug("получение заявки по id")
        return Invoice(id='2344', status='delete', data=InvoiceDataType(user_id=3203))


def eternity_cycle(db_client: DbClient):
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
