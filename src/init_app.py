from telegram.ext import Application

from src.services.db_client import DbClient
from src.settings import settings

application = Application.builder().token(settings.token).build()

db_client = DbClient(f'mongodb://{settings.db_user}:{settings.db_password}@localhost:27017/')