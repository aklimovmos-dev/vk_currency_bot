import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("VK_TOKEN")

if not TOKEN:
    raise ValueError("Не найден VK_TOKEN в файле .env")