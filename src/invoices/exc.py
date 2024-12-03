class InvalidInvoice(Exception):
    def __init__(self, message='Заявка не может быть отправлена дальше'):
        super().__init__(message)


class ServerProblem(Exception):
    def __init__(self, message='Ошибка сервера'):
        super().__init__(message)
