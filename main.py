from src.core import start_app
from src.logger import init_logger


def main() -> None:

    init_logger()
    start_app()


if __name__ == '__main__':
    main()
