import whisper
import os

from app.utils.logger import logger


model = whisper.load_model(os.getenv("WHISPER_MODEL"))


def transcribe_audio(file_path):

    logger.info("Starting audio transcription...")

    result = model.transcribe(
        file_path,
        initial_prompt="""
        Ini adalah meeting kerja profesional.

        Fokus pada:
        - diskusi proyek
        - timeline
        - technical discussion
        - action items
        - keputusan meeting
        - nama tools teknologi
        - nama produk
        - istilah IT dan bisnis
        """
    )

    logger.info("Audio transcription completed.")

    return result["text"]