import threading

from src.init_app import application
from src.invoices.simple_server import run_finish_invoice_server
from src.settings import settings
from src.handlers import conv_handler
from src.invoices.core import eternity_cycle


def start_app():
    thread = threading.Thread(target=eternity_cycle)
    thread.start()
    server_thread = threading.Thread(target=run_finish_invoice_server, args=(settings.bot_port,))
    server_thread.start()
    application.add_handler(conv_handler)
    application.run_polling()

