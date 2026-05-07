import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBSITE_URL = "https://college-ripo.by/uchashhimsya/zameny-v-raspisanii/"

CURR_DIR = os.path.dirname(os.path.abspath(__file__))
LOGS_DIR = os.path.join(CURR_DIR, "logs")

FOLDER_PATH = "/app/downloads_pdf"

DB_PATH = "/app/users.db"
