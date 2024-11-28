from telegram.ext import Application

from src.settings import settings

application = Application.builder().token(settings.token).build()

