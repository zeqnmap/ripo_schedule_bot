import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBSITE_URL= 'https://dev.remont-trimmera.by/uchashhimsya/zameny-v-raspisanii/'

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(CURR_DIR, 'logs')

# FOLDER_PATH = '/home/user/bot/downloads_pdf'
FOLDER_PATH = '/Users/yaroslavmanko/PycharmProjects/ripo_schedule_bot/downloads_pdf'
CURR_DATE = datetime.now().date()

DB_PATH = '/Users/yaroslavmanko/PycharmProjects/ripo_schedule_bot/users.db'
LOG_LEVEL = "INFO"
LOG_FILE = ""
