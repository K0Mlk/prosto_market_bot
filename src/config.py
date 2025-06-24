import os
from dotenv import load_dotenv

load_dotenv()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

class Config:
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    DB_CONFIG = {
        'host': os.getenv('DB_HOST'),
        'port': os.getenv('DB_PORT'),
        'user': os.getenv('DB_USER'),
        'password': os.getenv('DB_PASSWORD'),
        'database': os.getenv('DB_NAME')
    }
    SUPPORT_CHAT_ID = os.getenv('SUPPORT_CHAT_ID')
    TELEGRAM_CHANNEL_LINK = os.getenv('TELEGRAM_CHANNEL_LINK')
    PDF_MAP = {
        'barcode': os.path.join(BASE_DIR, 'static/Белый экран.pdf'),
        'screen': os.path.join(BASE_DIR, 'static/Черный экран.pdf'),
        'bank': os.path.join(BASE_DIR, 'static/Нет связи с банком.pdf')
    }