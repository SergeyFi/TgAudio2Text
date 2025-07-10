import asyncio
import logging
import tempfile
import os
import subprocess
from telethon import TelegramClient, events
from app.config import API_ID, API_HASH, SESSION_NAME, TARGET_USERS
from app.transcriber import transcribe


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
                voice_path_ogg = tmp_file.name

            # Save voice message
            try:
                await msg.download_media(file=voice_path_ogg)
                logging.info(f"Voice message saved in: {voice_path_ogg}")
            except Exception as e:
                logging.error(f"Error downloading voice: {e}")
                return
            
            # Convert .ogg to .wav
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_wav_file:
                voice_path_wav = tmp_wav_file.name

            try:
                subprocess.run(
                    ["ffmpeg", "-y", "-i", voice_path_ogg, "-ar", "16000", "-ac", "1", voice_path_wav],
                    check=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
                logging.info(f"Converted to WAV: {voice_path_wav}")
                
            except subprocess.CalledProcessError as e:
                logging.error(f"ffmpeg failed: {e}")
                return
            finally:
                os.remove(voice_path_ogg)
            
            # Decrypting and sending the message
            try:
                text = transcribe(voice_path_wav)
                logging.info(f"Transcript: {text}")

                await client.send_message(entity=sender_name, message=text, reply_to=msg.id)

            except Exception as e:
                logging.error(f"Decryption error: {e}")
            finally:
                os.remove(voice_path_wav)

    logging.info("Waiting for incoming messages...")
    await client.run_until_disconnected()

if __name__ == "__main__":
    asyncio.run(main())
