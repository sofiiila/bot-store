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


@app.route('/execute_function', methods=['POST'])
def execute_my_function():
    """
    invoices
    :return:
    """
    # Получаем данные из запроса
    data = request.json
    id = data['id']
    # TODO я бы переназвал тогда тип, меня смущает что какой-то last
    invoice: InvoiceType = InvoiceLookUp(base_url="base_url",
                                         db_client='db_client').get_invoice_by_id(id)
    if invoice:
        invoice.delete()
        return jsonify({"message": "Инвойс удален"})
    else:
        logger.error('такого id не существует')
        return jsonify({"error": "Инвойс не найден"}), 404


def run_finish_invoice_server(port: int):
    """ func"""
    app.run(port=port)


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    thread = threading.Thread(target=eternity_cycle)
    thread.start()
    server_thread = threading.Thread(target=app.run(port=8000))
    server_thread.start()
