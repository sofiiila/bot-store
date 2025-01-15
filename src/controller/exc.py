"""
exeption
"""

class BaseAppException(Exception):
    pass


class InvalidInvoice(BaseAppException):
    """
    exeption
    """
    def __init__(self, message='Заявка не может быть отправлена дальше'):
        super().__init__(message)


class ServerProblem(BaseAppException):
    """
    exeptions
    """
    def __init__(self, message='Ошибка сервера'):
        super().__init__(message)


class InvoiceNotExist(BaseAppException):
    pass
