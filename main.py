"""
main
"""
from src.start_app import start_app
from src.logger import init_logger

init_logger()


def main() -> None:
    """main"""
    start_app()


# TODO добавить все докстринги в проект и все типы
# TODO после этого провести проверку статическим типизатором mypy и линтером pylint
if __name__ == '__main__':
    main()


#TODO перенести схему бота в документацию и документацию обновить
#TODO добавить актуальные схемы бота
#TODO нет возможности запустить одной командой pylint
# (надо настроить pylint так чтобы он запускался pylint . и игнорировал venv)
#TODO dowloads удалить
#TODO docker-compose обычный проверить чтобы запускался
