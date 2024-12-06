from src.core import start_app
from src.logger import init_logger

init_logger()


def main() -> None:
    start_app()


# TODO добавить все докстринги в проект и все типы
# TODO провести проверку статическим типизатором mypy и линтером pylint
if __name__ == '__main__':
    main()
