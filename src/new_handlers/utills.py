import logging

from telegram import InlineKeyboardMarkup
from src.init_app import controller, Invoice

logger = logging.getLogger(__name__)


def construct_message_in_invoice(message: str, invoice: Invoice | None = None, step: str | None = None):
    if step is None:
        step = ""
    else:
        step = f"\nШаг: {step}\n\n"

    if invoice is None:
        invoice = ""
    else:
        invoice = f"Заявка № {invoice.invoice_id}\n"

    return f"{invoice}{step}{message}"


async def basic_handler_for_step_in_question_list(context, update, inline_buttons, log_message,
                                                  message,
                                                  step: str | None = None,
                                                  is_invoice: bool = True
                                                  ):
    keyboard = InlineKeyboardMarkup(inline_buttons)
    if update.message:
        query = update.message
        obj_for_reply = update.message
    else:
        query = update.callback_query
        await query.answer()
        obj_for_reply = update.callback_query.message
    user = query.from_user
    logger.info(log_message, user.username)
    invoice: None = None
    if is_invoice:
        invoice: Invoice = controller.update_document_for_user_id(query.from_user.id)
    await obj_for_reply.reply_text(
        construct_message_in_invoice(invoice=invoice, message=message, step=step),
        reply_markup=keyboard
    )
