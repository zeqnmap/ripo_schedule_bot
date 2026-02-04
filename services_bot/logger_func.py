import os
import logging
from config import LOGS_DIR


class LevelFileHandler(logging.Handler):
    def __init__(self,  base_name="", logs_dir="logs"):
        super().__init__()
        self.base_name = base_name
        self.logs_dir = logs_dir

        os.makedirs(LOGS_DIR, exist_ok=True)

        log_format = "%(levelname)s | %(name)s | %(asctime)s | %(lineno)d | %(message)s"
        formatter = logging.Formatter(log_format)
        self.setFormatter(formatter)

    def emit(self, record):
        level = record.levelname.lower()
        filename = os.path.join(self.logs_dir, f"{self.base_name}_{level}.log")

        message = self.format(record)

        with open(filename, 'a', encoding='utf-8') as file:
            file.write(message + '\n')


def setup_logger(name):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    handler = LevelFileHandler(base_name="bot", logs_dir=LOGS_DIR)
    handler.setLevel(logging.DEBUG)

    logger.addHandler(handler)
    return logger