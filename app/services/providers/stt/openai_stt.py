from openai import OpenAI
import os

from app.utils.logger import logger

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


def openai_transcribe(file_path: str) -> str:

    logger.info("Starting OpenAI transcription...")

    with open(file_path, "rb") as audio_file:

        transcription = client.audio.transcriptions.create(
            file=audio_file,
            model="gpt-4o-mini-transcribe",
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

    logger.info("OpenAI transcription completed.")

    return transcription.text