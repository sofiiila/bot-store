from telegram.ext import ConversationHandler, CommandHandler, MessageHandler, filters

from .handler_types import WRITE, ORDER, TZ, FILES, DEADLINE, QUESTION, CONTACTS, ASK_MORE, CONTINUE_OR_NEW
from .start import start
from .menu import menu
from .question import question
from .order import order
from .tz import tz
from .files import files
from .skip_files import skip_files
from .deadline import deadline
from .contacts import contacts
from .cancel import cancel
from .skip_deadline import skip_deadline
from .skip_tz import skip_tz
from .skip_question import skip_question
from .skip_contacts import skip_contacts
from .ask_more import ask_more

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        WRITE: [MessageHandler(filters.TEXT & ~filters.COMMAND, menu)],
        ORDER: [MessageHandler(filters.TEXT & ~filters.COMMAND, order)],
        TZ: [MessageHandler(filters.TEXT & ~filters.COMMAND, tz), CommandHandler("skip", skip_tz)],
        FILES: [MessageHandler(filters.Document.ALL, files), CommandHandler("skip", skip_files)],
        DEADLINE: [MessageHandler(filters.TEXT & ~filters.COMMAND, deadline), CommandHandler("skip", skip_deadline)],
        QUESTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, question), CommandHandler("skip", skip_question)],
        CONTACTS: [MessageHandler(filters.TEXT & ~filters.COMMAND, contacts), CommandHandler("skip", skip_contacts)],
        ASK_MORE: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_more)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)