import os
from dotenv import load_dotenv
from datetime import timezone, timedelta

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
BOT_TIMEZONE = timezone(timedelta(hours=9))

if not TOKEN:
    raise ValueError("No TELEGRAM_BOT_TOKEN found in environment variables")