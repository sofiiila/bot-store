"""
module start app
"""
import threading

from src.init_app import application, controller
from src.settings import settings
from src.new_handlers import conv_handler
from src.web.server import run_finish_invoice_server


def start_app() -> None:
    """
    Запуск тредов:
    1. Отслеживание таймаутов заявок.
    2. Цикл отправки заявок.
    3. Сервер для приема запросов от CRM.
    4. Бот сбора заявок.
    """
    timer_thread = threading.Thread(target=controller.check_timeout_iteration)
    timer_thread.start()
    # thread = threading.Thread(target=controller.eternity_cycle_iteration)
    # thread.start()
    # server_thread = threading.Thread(target=run_finish_invoice_server, args=(settings.bot_port,))
    # server_thread.start()
    application.add_handler(conv_handler)
    application.run_polling()
