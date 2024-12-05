import logging

from src.invoices.invoice import Invoice
from src.services.db_client_types import CategoriesEnum

InvoiceType = Invoice | None

logger = logging.getLogger(__name__)


class InvoiceLookUp:
    """
    Распорядитель заявок для верхнеуровневых ф-й
    """
    def __init__(self, base_url, db_client):
        self.__base_url = base_url
        self.db_client = db_client

    def _create_invoice(self, data):
        return Invoice(data, base_url=self.__base_url, db_client=self.db_client)

    def get_oldest_invoice(self) -> InvoiceType:
        """
        возвращает самую старую заявку из очереди или None
        :return: obj Invoice
        """
        result = self.db_client.list(
            filter_query={"category": CategoriesEnum.queue},
            sort_query={"start_date": 1})
        if result:
            logger.debug("Получена заявка с ID: %s",  result[0].id)
            return self._create_invoice(result[0])
        return None

    def get_invoice_by_id(self, id) -> Invoice | None:
        """
        Возвращает заявку которую пора удалять
        :param id:
        :return: obj Invoice
        """
        logger.debug("получение заявки по id")
        result = self.db_client.list(
            filter_query={"_id": id},
        )
        if result:
            return self._create_invoice(result)
        return None

    def get_all_new_invoices(self):
        results = self.db_client.list(
            filter_query={"category": CategoriesEnum.new})
        new_invoices=[]

        if results:
            for result in results:
                new_invoices.append(self._create_invoice(result))

        return new_invoices
