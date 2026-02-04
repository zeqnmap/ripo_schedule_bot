import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import time
from selenium import webdriver
from config import WEBSITE_URL, FOLDER_PATH
from services_bot.logger_func import setup_logger
from selenium.webdriver.common.by import By

logger = setup_logger('get_schedule_logger')
url = WEBSITE_URL


class ScheduleDownloader:
    """Класс для скачивания расписание с сайта"""

    def __init__(self, download_dir=None) -> None:
        """
        Конструктор, где указывается путь до папки и идет настройка опций и драйвера
        для работы с функцией js_click_and_save()
        """
        IS_SERVER = os.path.exists('/root/bot')

        if download_dir is None:
            if IS_SERVER:
                self.download_dir = '/root/bot/downloads_pdf'
            else:
                self.download_dir = os.path.join(FOLDER_PATH)
        else:
            self.download_dir = download_dir

        # Создаем директорию если не существует
        os.makedirs(self.download_dir, exist_ok=True)

        options = webdriver.ChromeOptions()

        prefs = {
            "download.default_directory": self.download_dir,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True,
            "safebrowsing.enabled": True,
            "profile.default_content_settings.popups": 0,
            "profile.content_settings.exceptions.automatic_downloads.*.setting": 1
        }
        options.add_experimental_option("prefs", prefs)

        # опции без UI + user-agent
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        try:
            self.driver = webdriver.Chrome(options=options)
        except Exception as e:
            logger.error(f"Ошибка с ChromeDriver: {e}")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        """Закрывает драйвер браузера"""
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()
        self.driver = None

    def get_latest_downloaded_file(self) -> str:
        """
        Возвращает путь к последнему скачанному файлу
        """
        time.sleep(2)

        files = os.listdir(self.download_dir)

        if not files:
            return "Ошибка: файл не скачан"

        files = [os.path.join(self.download_dir, f) for f in files]
        files.sort(key=os.path.getmtime, reverse=True)

        latest = files[0]

        if latest.endswith(('.crdownload', '.tmp', '.part')):
            return "Ошибка: файл еще качается"

        return latest

    def cleanup_old_files(self, max_files):
        """
        Удаляет старые файлы, если их больше max_files.
        Оставляет только max_files самых новых.
        """
        try:
            files = [os.path.join(self.download_dir, f) for f in os.listdir(self.download_dir)]

            files = [f for f in files if os.path.isfile(f)]

            if len(files) <= max_files:
                return

            files.sort(key=os.path.getmtime)

            files_to_delete = files[:len(files) - max_files]

            for file_path in files_to_delete:
                try:
                    os.remove(file_path)
                    logger.info(f"Удалил старый файл: {os.path.basename(file_path)}")
                except Exception as e:
                    logger.error(f"Не удалось удалить {file_path}: {e}")

        except Exception as e:
            logger.error(f"Ошибка в cleanup_old_files: {e}")

    @classmethod
    def rename_file(cls, file_path):
        """Переименовывает файл в 'Расписание (1).pdf' и т.д."""
        import os

        try:
            dir_name = os.path.dirname(file_path)
            ext = os.path.splitext(file_path)[1] or '.pdf'

            # Ищем свободное имя
            counter = 1
            while True:
                if counter == 1:
                    new_name = f"Расписание{ext}"
                else:
                    new_name = f"Расписание ({counter}){ext}"

                new_path = os.path.join(dir_name, new_name)

                if not os.path.exists(new_path):
                    os.rename(file_path, new_path)
                    return new_path

                counter += 1

        except Exception as e:
            logger.error(f"Ошибка: {e}")
            return file_path

    def js_click_and_save(self) -> str:
        """
        Функция, которая с помощью selenium тыкает на нужные кнопки.
        Возвращает путь к скачанному файлу
        """
        downloaded_file_path = None

        try:
            self.driver.get(url)
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            button = self.driver.find_element(By.XPATH,
                       '/html/body/div[1]/div[2]/div/div[2]/div/div[1]/div/div/main/article/div/div/a[2]')

            button.click()
            time.sleep(1)
            downloaded_file_path = self.get_latest_downloaded_file()

            if downloaded_file_path and "Ошибка" not in downloaded_file_path:
                downloaded_file_path = self.rename_file(downloaded_file_path)

            self.cleanup_old_files(max_files=15)

        except Exception as e:
            logger.error(f"Ошибка в блоке функции js_click {e}")

        return downloaded_file_path


def get_schedule():
    """Скачивает расписание путем вызова основной функции"""
    try:
        with ScheduleDownloader() as downloader:
            return downloader.js_click_and_save()
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        return None


if __name__ == "__main__":
    result_ = get_schedule()
    print(f"Результат: {result_}")