import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = "TgAudio2Text"
FILTER_USERS = os.getenv("FILTER_USERS", "false").lower() == "true"
TARGET_USERS = os.getenv("TARGET_USERS", "").split(",") if FILTER_USERS else None
MODEL_SIZE = os.getenv("MODEL_SIZE", "tiny").lower()
