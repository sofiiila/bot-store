import logging
import threading
import time

from invoices.sdsd import Invoice


LastInvoiceLookUpType = Invoice | None

logger = logging.getLogger(__name__)


class InvoiceLookUp():
    def get_last_invoice(self) -> LastInvoiceLookUpType:
        logger.debug("Функуия определяющая последнюю заявку")
        return Invoice(id='3203', status='in-progress')

    def get_invoice_by_id(self, id) -> LastInvoiceLookUpType:
        logger.debug("получение заявки по id")
        return Invoice(id='2344', status='delete')


def eternity_cycle():
    logger.debug("запуск бесконечного цикла")
    while True:
        invoice: LastInvoiceLookUpType = InvoiceLookUp().get_last_invoice()
        if invoice is not None:
            invoice.prepare()
        time.sleep(1)


def main():
    logging.basicConfig(level=logging.DEBUG)
    thread = threading.Thread(target=eternity_cycle())
    thread.start()


if __name__ == "__main__":
    main()