"""
module server
"""
import logging
import threading

from flask import Flask, request, jsonify

from src.invoices.core import eternity_cycle
from src.invoices.invoice_look_up import InvoiceLookUp, InvoiceType

app = Flask(__name__)

logger = logging.getLogger(__name__)


# pylint: disable=redefined-builtin
@app.route('/execute_function', methods=['POST'])
def execute_my_function() -> tuple[str, int]:
    """
    Обработка инвойсов
    :return:
    """
    # Получаем данные из запроса
    data = request.json
    if data is None:
        return "Request body is empty", 400

    # pylint: disable=unsubscriptable-object
    try:
        id = data['id']
    except KeyError as e:
        logger.error('KeyError: %s', e)
        return f'Missing required key "id"', 400

    # TODO я бы переназвал тогда тип, меня смущает что какой-то last
    invoice: InvoiceType = InvoiceLookUp(base_url="base_url",
                                         db_client='db_client').get_invoice_by_id(id)
    if invoice:
        invoice.delete()
        return "Инвойс удален", 200

    logger.error('такого id не существует')
    return "Инвойс не найден", 404


def run_finish_invoice_server(port: int) -> None:
    """ func"""
    app.run(port=port)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    thread = threading.Thread(target=eternity_cycle)
    thread.start()
    run_finish_invoice_server(8000)
