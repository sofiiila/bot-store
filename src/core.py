from src.handlers import conv_handler
from src.init_app import application


def start_app():

    application.add_handler(conv_handler)
    application.run_polling()