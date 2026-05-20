import os
import time
from typing import Dict, List

from config import FOLDER_PATH
from services_bot.logger_func import setup_logger

logger = setup_logger("size_control_logger")

FLAG: Dict = {"FLAG": False}


def take_new_file() -> str:
    """
    Берет два последних файла из всей папки, сравнивает их по размеру
    и если последний файл отличается по размеру от предыдущего, следовательно, он новый.
    :return
        str(путь к файлу)
    """
    time.sleep(305)
    all_paths: List[str] = []

    for file in os.listdir(FOLDER_PATH):
        folder_path = os.path.join(FOLDER_PATH, file)
        all_paths.append(folder_path)
    sorted_folder_path = sorted(all_paths, key=os.path.getmtime)

    two_latest_files = sorted_folder_path[-2:]

    file1, file2 = two_latest_files

    get_size_1 = os.path.getsize(file1)
    get_size_2 = os.path.getsize(file2)

    if get_size_2 != get_size_1:
        FLAG["FLAG"] = True
        return file2

    else:
        FLAG["FLAG"] = False
        return file2
