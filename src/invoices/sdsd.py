import logging

logger = logging.getLogger(__name__)


class ApiClient:
    def post(self) -> int:
        return 422


class Invoice:
    def __init__(self, id, status):
        self.id = id
        self.status = status
        self.api_client = ApiClient()

    @classmethod
    def create(cls):
        """
        будет вызываться в момеент когда заполнено в боте
        :return:
        """
        logger.debug("метод create")

    def delete(self):
        logger.debug("Я удаляю ")
        pass

    def in_progress(self):
        logger.debug("Вызван ин прогрес")
        pass

    def is_invalid(self):
        logger.debug("инвалид здесб")
        pass

    def prepare(self):
        logger.debug("обрабатывается статус ответа")
        result = self.api_client.post()
        logger.debug(f"Код ответа: {result}")
        match result:
            case 200:
                self.in_progress()
            case 422:
                self.is_invalid()

