"""
init
"""
from telegram.ext import Application
from src.settings import settings
# pylint: disable=unused-import
from .controller import Controller, Invoice
from .db_client.core import DbClient


application = Application.builder().token(settings.token).build()
controller = Controller(
    db_client=DbClient(
        db_user=settings.db_user,
        db_password=settings.db_password,
        host=settings.db_container_name
    ),
    base_url=settings.base_url,
    overdue_time_sleep=settings.overdue_time_sleep,
    queue_time_sleep=settings.queue_time_sleep,
    is_overdue_time=settings.is_overdue_time
)
