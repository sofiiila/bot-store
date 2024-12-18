"""
module start app
"""
import threading

from src.init_app import application
# from src.invoices.simple_server import run_finish_invoice_server
# from src.settings import settings
from src.new_handlers import conv_handler
# from src.invoices.core import eternity_cycle, check_timeout


def start_app():
    """
    запуск тредов
    :return:
    """
    # timer_thread = threading.Thread(target=check_timeout)
    # timer_thread.start()
    # thread = threading.Thread(target=eternity_cycle)
    # thread.start()
    # server_thread = threading.Thread(target=run_finish_invoice_server, args=(settings.bot_port,))
    # server_thread.start()
    application.add_handler(conv_handler)
    application.run_polling()
