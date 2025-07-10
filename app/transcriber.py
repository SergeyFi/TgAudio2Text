import logging
import time
import os
import tempfile
import subprocess
from faster_whisper import WhisperModel, BatchedInferencePipeline
from app.config import MODEL_SIZE

model = WhisperModel(MODEL_SIZE, device="cpu", compute_type="int8")
batched_model = BatchedInferencePipeline(model=model)

logging.basicConfig(level=logging.INFO)

def transcribe(audio_path: str) -> str:
    clean_audio_path = denoise_audio(audio_path)

    segments, info = batched_model.transcribe(
        clean_audio_path, 
        beam_size=5,
        language="ru",
        vad_filter=True,
        temperature=0.1,
        )
    
    start_time = time.time()

    text = ""
    for segment in segments:
        text += segment.text

    end_time = time.time()
    
    elapsed_time = end_time - start_time
    speed_ratio = info.duration / elapsed_time
    logging.info(f"Transcription: {elapsed_time:.2f} sec, audio duration: {info.duration:.2f} sec, speed: {speed_ratio:.2f}x")

    return text


def denoise_audio(input_path: str) -> str:
    tmp_fd, clean_path = tempfile.mkstemp(suffix=".wav")
    os.close(tmp_fd)
    try:
        subprocess.run([
            "sox", input_path, clean_path,
            "highpass", "100",
            "lowpass", "4000",
            "norm",
            "gain", "-n"
        ], check=True)
        return clean_path
    except subprocess.CalledProcessError as e:
        logging.warning(f"Error clearing audio: {e}")
        return input_path
