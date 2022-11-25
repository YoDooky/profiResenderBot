import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

TOKEN = os.getenv('TOKEN')
API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')
PHONE = os.getenv('PHONE')

WEBHOOK_PATH = f"/main/{TOKEN}"
APP_URL = os.getenv('APP_URL')
WEBHOOK_URL = APP_URL + WEBHOOK_PATH
