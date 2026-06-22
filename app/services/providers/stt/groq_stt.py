from groq import Groq
import os

from app.utils.logger import logger

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)


def groq_transcribe(file_path: str) -> str:

    logger.info("Starting Groq transcription...")

    with open(file_path, "rb") as audio_file:

        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="whisper-large-v3-turbo",
            language="id",
            prompt="""
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

    logger.info("Groq transcription completed.")

    return transcription.text