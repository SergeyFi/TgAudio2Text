from telethon import TelegramClient, events
from config import API_ID, API_HASH, SESSION_NAME, TARGET_USERS
from transcriber import transcribe
import asyncio
import logging
import tempfile
import os


logging.basicConfig(level=logging.INFO)

async def main():
    client = TelegramClient(SESSION_NAME, API_ID, API_HASH)
    await client.start()

    @client.on(events.NewMessage(from_users=TARGET_USERS))
    async def handler(event):
        msg = event.message
        sender = await event.get_sender()
        sender_name = getattr(sender, "username", "Unknown")

        if msg.voice:
            logging.info(f"Received a voice message from {sender_name}")

            # Create a temporary file with the extension .ogg
            with tempfile.NamedTemporaryFile(suffix=".ogg", delete=False) as tmp_file:
                voice_path = tmp_file.name

            # Save voice message
            try:
                await msg.download_media(file=voice_path)
                logging.info(f"Voice message saved in: {voice_path}")
            except Exception as e:
                logging.error(f"Error downloading voice: {e}")
                return
            
            # Decrypting and sending the message
            try:
                text = transcribe(voice_path)
                logging.info(f"Transcript: {text}")

                await client.send_message(entity=sender_name, message=text, reply_to=msg.id)

            except Exception as e:
                logging.error(f"Decryption error: {e}")
            finally:
                os.remove(voice_path)

    logging.info("Waiting for incoming messages...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
