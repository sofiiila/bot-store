import logging
from pathlib import Path

from telegram import InlineKeyboardMarkup
from src.controller.invoice import Invoice
from src.init_app import controller


logger = logging.getLogger(__name__)



async def save_media(media, user_id, media_type, file_extension):
    """
    Сохранение медиафайлов в указанный путь.
    """
    invoice = controller.update_document_for_user_id(user_id=user_id)
    file = await media.get_file()
    file_path = Path(invoice.files_path) / f"{media_type}_{media.file_id}{file_extension}"
    file_path.parent.mkdir(parents=True, exist_ok=True)
    await file.download_to_drive(file_path)
    logger.info("%s сохранено в: %s", media_type.capitalize(), file_path)


def construct_message_in_invoice(message: str, invoice: Invoice | None = None,
                                 step: str | None = None):
    """
    Формирует сообщение с информацией о заявке и текущем шаге.
    """
    step_text = f"\nШаг: {step}\n\n" if step is not None else ""
    invoice_text = f"Заявка № {invoice.invoice_id}\n" if invoice is not None else ""
    return f"{invoice_text}{step_text}{message}"


# pylint: disable=too-many-arguments
# pylint: disable=too-many-positional-arguments
async def basic_handler_for_step_in_question_list(update, inline_buttons,
                                                  log_message,
                                                  message,
                                                  step: str | None = None,
                                                  is_invoice: bool = True
                                                  ):
    """
    Базовый обработчик для шагов, в которых пользователь выбирает один из вариантов.
    """
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
    invoice: None = None  # type: ignore[no-redef]
    if is_invoice:
        invoice: Invoice = controller.update_document_for_user_id(  # type: ignore[no-redef]
            query.from_user.id)
    await obj_for_reply.reply_text(
        construct_message_in_invoice(invoice=invoice, message=message, step=step),
        reply_markup=keyboard
    )
