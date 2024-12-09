"""
init
"""
from telegram.ext import Application

from src.settings import settings
from .invoices.invoice_look_up import InvoiceLookUp
from .services.core import DbClient

application = Application.builder().token(settings.token).build()
db_client = DbClient(settings.db_user, settings.db_password, host=settings.db_container_name)
invoice_look_up = InvoiceLookUp(settings.base_url, db_client)
