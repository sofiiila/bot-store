import logging


def init_logger():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO)
    logging.getLogger("httpx").setLevel(logging.WARNING)


logger = logging.getLogger(__name__)