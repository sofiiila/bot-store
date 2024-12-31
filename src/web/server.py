"""
module server
"""
import logging
from flask import Flask, request
from src.init_app import controller
from src.controller.exc import InvoiceNotExist

app = Flask(__name__)

logger = logging.getLogger(__name__)


# pylint: disable=redefined-builtin
@app.route('/execute_function', methods=['POST'])
def execute_my_function() -> tuple[str, int]:
    """
    Обработка инвойсов
    :return:
    """
    data = request.json
    if data is None:
        return "Request body is empty", 400
    try:
        controller.finish_invoice(invoice_id=data['id'])
    except KeyError as e:
        logger.error('KeyError: %s', e)
        return 'Missing required key "id"', 400
    except InvoiceNotExist:
        logger.error('такого id не существует')
        return "Инвойс не найден", 404


def run_finish_invoice_server(port: int) -> None:
    """ func"""
    app.run(port=port)