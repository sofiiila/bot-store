"""
init
"""
from telegram.ext import Application
from src.settings import settings
from .controller.core import Controller
from .db_client.core import DbClient


application = Application.builder().token(settings.token).build()
controller = Controller(
    db_client=DbClient(settings.db_user, settings.db_password, host=settings.db_container_name),
    base_url=settings.base_url
)
