import os
import whisper

from app.utils.logger import logger

# load model sekali saat aplikasi startup
model = whisper.load_model(
    os.getenv("WHISPER_MODEL", "base")
)


def local_whisper_transcribe(file_path: str) -> str:
    """
    Transcribe audio menggunakan local OpenAI Whisper.
    """

    logger.info("Starting local Whisper transcription...")

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

    logger.info("Local Whisper transcription completed.")

    return result["text"]