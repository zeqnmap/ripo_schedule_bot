import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import datetime
import threading
import time
from services_bot.logger_func import setup_logger
from services_bot.get_schedule import get_schedule

logger = setup_logger("time_logger")


def launch_control_get_schedule():
    """
    Контролирует запуск функции получение расписания в отдельном потоке и в нужное время,
    чтобы не останавливать работу основной программы
    """
    while True:
        current_time = datetime.datetime.now().time()

        if datetime.time(7, 50) <= current_time < datetime.time(11, 0):
            logger.info(f"Запуск обновления расписания запущен в {current_time}")
            get_schedule()
            time.sleep(300)

        elif datetime.time(21, 0) <= current_time < datetime.time(22, 0):
            logger.info(f"Запуск обновления расписания запущен в {current_time}")
            get_schedule()
            time.sleep(300)

        elif datetime.time(6, 30) <= current_time < datetime.time(7, 30):
            logger.info(f"Запуск обновления расписания запущен в {current_time}")
            get_schedule()
            time.sleep(300)

        time.sleep(1)


time_thread = threading.Thread(target=launch_control_get_schedule)
