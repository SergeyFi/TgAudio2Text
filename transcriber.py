import logging
from faster_whisper import WhisperModel
import time

model_size = "tiny"
model = WhisperModel(model_size, device="cpu", compute_type="int8")

logging.basicConfig(level=logging.INFO)

def transcribe(audio_path: str) -> str:
    segments, info = model.transcribe(audio_path, beam_size=5)
    
    start_time = time.time()

    text = ""
    for segment in segments:
        text += segment.text

    end_time = time.time()
    
    elapsed_time = end_time - start_time
    speed_ratio = info.duration / elapsed_time
    logging.info(f"Transcription: {elapsed_time:.2f} sec, audio duration: {info.duration:.2f} sec, speed: {speed_ratio:.2f}x")

    return text