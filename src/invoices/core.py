import logging
import threading
import time

from src.init_app import invoice_look_up
from src.invoices.invoice import Invoice
from src.invoices.invoice_look_up import InvoiceType

logger = logging.getLogger(__name__)


def eternity_cycle():
    """
    Цикл обрабатывающий заявки из очереди
    :return:
    """
    logger.debug("Запущена очередь.(беск цикл)")
    while True:
        invoice: InvoiceType = invoice_look_up.get_oldest_invoice()
        if invoice is not None:
            invoice.prepare()
        time.sleep(1)


def check_timeout():
    logger.debug("Запущен таймаут.")
    while True:
        invoices: list[Invoice] = invoice_look_up.get_all_new_invoices()
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
