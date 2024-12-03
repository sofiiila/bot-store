from telegram.ext import Application
from .services.core import DbClient
from src.settings import settings

application = Application.builder().token(settings.token).build()
db_client = DbClient(settings.db_user, settings.db_password, host=settings.db_container_name)