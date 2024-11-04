import logging
from pathlib import Path
from datetime import datetime
import sys


# Функция для перехвата всех необработанных исключений
def handle_exception(exc_type, exc_value, exc_traceback):
    if issubclass(exc_type, KeyboardInterrupt):
        # Игнорируем прерывание с клавиатуры (Ctrl+C)
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    logging.error("Необработанное исключение", exc_info=(exc_type, exc_value, exc_traceback))


def set(prefix: str = "log"):
    logs_path = Path("logs")
    logs_path.mkdir(parents=True, exist_ok=True)
    log_file_name = datetime.now().strftime(f"{prefix}_%Y-%m-%d_%H-%M-%S.log")
    log_file_path = logs_path / log_file_name
    file_log = logging.FileHandler(log_file_path.absolute())
    console_out = logging.StreamHandler()

    logging.basicConfig(
        handlers=(file_log, console_out),
        level=logging.INFO,
        format="%(levelname)s %(asctime)s %(module)s - %(funcName)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    sys.excepthook = handle_exception
