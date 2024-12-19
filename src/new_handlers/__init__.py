from telegram.ext import ConversationHandler, CommandHandler, \
    CallbackQueryHandler, MessageHandler, filters

from src.new_handlers.handler_types import START, ORDER, WRITE, CONTACTS
from src.new_handlers.cancel import cancel
from src.new_handlers.start import start
from src.new_handlers.order import order
from src.new_handlers.write import write
from src.new_handlers.contacts import contacts


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        START: [
            CallbackQueryHandler(order,
                                 pattern="^" + str(ORDER) + "$"),
            CallbackQueryHandler(write,
                                 pattern="^" + str(WRITE) + "$")
        ],
        ORDER: [
        ],
        WRITE: [
            CallbackQueryHandler(contacts,
                                 pattern="^" + str(CONTACTS) + "$"),
            MessageHandler(filters.TEXT & ~filters.COMMAND, write),                     
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)
