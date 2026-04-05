import os
import time
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from config import WEBSITE_URL, FOLDER_PATH
from services_bot.logger_func import setup_logger

logger = setup_logger('get_schedule_logger')
url = WEBSITE_URL


class ScheduleDownloader:
    def __init__(self, download_dir=None):
        self.driver = None

        IS_SERVER = os.path.exists('/root/bot')
        if download_dir is None:
            if IS_SERVER:
                self.download_dir = '/app/downloads_pdf'
            else:
                self.download_dir = os.path.join(FOLDER_PATH)
        else:
            self.download_dir = download_dir
        os.makedirs(self.download_dir, exist_ok=True)

        options = webdriver.ChromeOptions()
        options.add_argument('--headless=new')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument(
            '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36')

        def _init_driver(max_retries=5, delay=5):
            for attempt in range(max_retries):
                try:
                    self.driver = webdriver.Remote(
                        command_executor='http://chrome:4444/wd/hub',
                        options=options
                    )
                    logger.info("Успешное подключение к Selenium Grid")
                    return
                except Exception as e:
                    logger.warning(f"Попытка {attempt+1}/{max_retries} не удалась: {e}")
                    if attempt < max_retries-1:
                        time.sleep(delay)
                    else:
                        logger.error("Не удалось подключиться к Selenium Grid")
                        self.driver = None
                        raise

        _init_driver()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()
        self.driver = None

    def get_latest_downloaded_file(self):
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
        try:
            files = [os.path.join(self.download_dir, f) for f in os.listdir(self.download_dir)]
            files = [f for f in files if os.path.isfile(f)]
            if len(files) <= max_files:
                return
            files.sort(key=os.path.getmtime)
            for file_path in files[:len(files)-max_files]:
                os.remove(file_path)
                logger.info(f"Старый файл удален: {os.path.basename(file_path)}")
        except Exception as e:
            logger.error(f"Ошибка в cleanup_old_files: {e}")

    @classmethod
    def rename_file(cls, file_path):
        try:
            dir_name = os.path.dirname(file_path)
            ext = os.path.splitext(file_path)[1] or '.pdf'
            counter = 1
            while True:
                new_name = f"Расписание{ext}" if counter == 1 else f"Расписание ({counter}){ext}"
                new_path = os.path.join(dir_name, new_name)
                if not os.path.exists(new_path):
                    os.rename(file_path, new_path)
                    return new_path
                counter += 1
        except Exception as e:
            logger.error(f"Ошибка при переименовании: {e}")
            return file_path

    def js_click_and_save(self):
        try:
            self.driver.get(url)
            time.sleep(2)
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            button = self.driver.find_element(By.XPATH,
                '/html/body/div[1]/div[2]/div/div[2]/div/div[1]/div/div/main/article/div/div/a[2]')
            file_url = button.get_attribute('href')
            if not file_url:
                logger.error("Не удалось получить URL файла")
                return None
            logger.info("Получен URL файла, скачиваю...")
            response = requests.get(file_url, stream=True)
            if response.status_code == 200:
                # Определяем имя файла из URL или используем стандартное
                filename = os.path.basename(file_url) or 'Расписание.pdf'
                file_path = os.path.join(self.download_dir, filename)
                with open(file_path, 'wb') as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                logger.info(f"Файл скачан: {file_path}")
                # Переименовываем и чистим старые файлы
                renamed_path = self.rename_file(file_path)
                self.cleanup_old_files(max_files=15)
                return renamed_path
            else:
                logger.error(f"Ошибка скачивания: статус {response.status_code}")
                return None
        except Exception as e:
            logger.error(f"Ошибка в js_click_and_save: {e}")
            return None


def get_schedule():
    try:
        with ScheduleDownloader() as downloader:
            return downloader.js_click_and_save()
    except Exception as e:
        logger.error(f"Ошибка: {e}")
        return None