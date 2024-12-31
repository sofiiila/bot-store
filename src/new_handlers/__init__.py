from telegram.ext import ConversationHandler, CommandHandler, \
    CallbackQueryHandler, MessageHandler, filters

from src.new_handlers.deadline import handle_user_deadline, deadline
from src.new_handlers.handler_types import START, ORDER, WRITE, CONTACTS, DEADLINE
from src.new_handlers.cancel import cancel
from src.new_handlers.start import start
from src.new_handlers.order import order, handle_user_tz
from src.new_handlers.write import write, handle_user_message
from src.new_handlers.contacts import contacts, handle_user_contacts

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
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_tz),
            CallbackQueryHandler(start, pattern="^" + str(START) + "$"),
            CallbackQueryHandler(deadline, pattern="^" + str(DEADLINE) + "$")
        ],
        WRITE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_message),
            CallbackQueryHandler(start, pattern="^" + str(START) + "$"),
        ],
        CONTACTS: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_contacts),
            CallbackQueryHandler(start, pattern="^" + str(START) + "$"),
        ],
        DEADLINE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, handle_user_deadline),
            CallbackQueryHandler(start, pattern="^" + str(START) + "$"),
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)]
)
