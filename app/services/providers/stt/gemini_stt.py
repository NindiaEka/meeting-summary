from google import genai
import os

from app.utils.logger import logger

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def gemini_transcribe(file_path: str) -> str:

    logger.info("Starting Gemini transcription...")

    uploaded_file = client.files.upload(
        file=file_path
    )

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            uploaded_file,
            """
            Transkripsikan audio ini ke bahasa Indonesia.

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
        ]
    )

    logger.info("Gemini transcription completed.")

    return response.text