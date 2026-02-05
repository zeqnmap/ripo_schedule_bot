import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBSITE_URL= 'https://dev.remont-trimmera.by/uchashhimsya/zameny-v-raspisanii/'

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(CURR_DIR, 'logs')

            # '/home/user/bot/downloads_pdf'
FOLDER_PATH = '/Users/yaroslavmanko/PycharmProjects/ripo_schedule_bot/downloads_pdf'

DB_PATH = '/Users/yaroslavmanko/PycharmProjects/ripo_schedule_bot/users.db'
