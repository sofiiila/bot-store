from telegram.ext import ConversationHandler, CommandHandler, \
    CallbackQueryHandler

from src.new_handlers.handler_types import START, ORDER
from src.new_handlers.cancel import cancel
from src.new_handlers.start import start
from src.new_handlers.order import order


conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start)],
    states={
        START: [
            CallbackQueryHandler(order,
                                 pattern="^" + str(ORDER) + "$")
        ],
        ORDER: []
    },
    fallbacks=[CommandHandler("stop", cancel)]
)
