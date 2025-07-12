from telethon import TelegramClient
import os
from dotenv import load_dotenv

load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_FILE = "TgAudio2Text.session"

client = TelegramClient(SESSION_FILE, API_ID, API_HASH)

print("Connecting to Telegram...")
client.start()

print(f"✅ Session successfully created and saved to file '{SESSION_FILE}'.")
client.disconnect()
