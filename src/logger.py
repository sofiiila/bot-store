"""
MODULE LOGGER sdmf
"""
import logging


def init_logger():
    """
    INIT LOGGER
    :return:
    """
    logging.basicConfig(
        format='%(asctime)s - [%(threadName)s] - %(name)s - %(levelname)s - %(message)s',
        level=logging.DEBUG)
    
    # TODO настроить логгирование в в файл и консоль. Сделать логи красивыми с помощью coloredlogs

    # TODO вынести в отдельную функцию disable_bad_loggers()
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("telegram._bot").setLevel(logging.WARNING)
    logging.getLogger("pymongo.topology").setLevel(logging.WARNING)
    logging.getLogger("pymongo.serverSelection").setLevel(logging.WARNING)
    logging.getLogger("pymongo.connection").setLevel(logging.WARNING)
    logging.getLogger("telegram.ext._conversationhandler").setLevel(logging.WARNING)
    logging.getLogger("telegram.ext._updater").setLevel(logging.WARNING)
    logging.getLogger("apscheduler.scheduler").setLevel(logging.WARNING)
    logging.getLogger("telegram.ext._application").setLevel(logging.WARNING)
    logging.getLogger("pymongo.command").setLevel(logging.WARNING)
    logging.getLogger("urllib3.connectionpool").setLevel(logging.WARNING)
    logging.getLogger("werkzeug").setLevel(logging.WARNING)
