import logging

from src.bot_types import InvoiceDataType

logger = logging.getLogger(__name__)


class CrmApiClient:
    """
    Клиент для отправки запросов к CRM
    """
    def try_send_invoice(self, invoice_data) -> int:
        return 422


class Invoice:
    """
    Класс для работы с заявками, определяет их статус и id
    """
    def __init__(self, id: str, status: str, data: InvoiceDataType):
        self.__id = id
        self.__status = status
        self.__api_client = CrmApiClient()
        self.__data = data

    def __is_invalid(self):
        """
        метод для заявок котрые получили 422 код ответа
        :return:
        """
        logger.debug("инвалид здесб")
        pass

    def __in_progress(self):
        """
        метод дающий заявке статус в процессе, она ждет когда CRM пришлет ready
        :return:
        """
        logger.debug("Вызван ин прогрес")
        pass

    @classmethod
    def create(cls):
        """
        будет вызываться в момеент когда заполнено в боте
        :return:
        """
        logger.debug("метод create")

    def delete(self):
        """
        метод удаляющий заявку из очереди, когда она уже попала в CRM
        :return:
        """
        logger.debug("Я удаляю ")
        pass

    def prepare(self):
        """
        метод решающий куда оптравится заявка после ответа от сервера
        :return:
        """
        logger.debug("обрабатывается статус ответа")
        result = self.__api_client.try_send_invoice(invoice_data=self.__data.dict())
        logger.debug(f"Код ответа: {result}")
        match result:
            case 200:
                self.__in_progress()
            case 422:
                self.__is_invalid()

