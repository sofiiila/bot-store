"""
инициализация обработчиков
"""
from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters

from .handler_types import WRITE, ORDER, TZ, FILES, DEADLINE, QUESTION, CONTACTS, ASK_MORE
from .start import start
from .menu import menu
from .question import question
from .order import order
from .tz import tz
from .files import files
from .deadline import deadline
from .contacts import contacts
from .cancel import cancel
from .ask_more import ask_more

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        WRITE: [MessageHandler(filters.TEXT & ~filters.COMMAND, menu)],
        ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, order)],
        TZ: [MessageHandler(filters.TEXT & ~filters.COMMAND, tz),
             CommandHandler("skip", tz)],
        FILES: [MessageHandler(filters.Document.ALL, files),
                CommandHandler("skip", files)],
        DEADLINE: [MessageHandler(filters.TEXT & ~filters.COMMAND, deadline),
                   CommandHandler("skip", deadline)],
        QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, question),
                   CommandHandler("skip", question)],
        CONTACTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, contacts),
                   CommandHandler("skip", contacts)],
        ASK_MORE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_more)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
