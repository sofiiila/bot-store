from src.core import start_app
from src.logger import init_logger

init_logger()

def main() -> None:
    start_app()


if __name__ == '__main__':
    main()
