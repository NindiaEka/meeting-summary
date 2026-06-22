import os

from app.services.providers.stt.local_whisper_stt import local_whisper_transcribe
from app.services.providers.stt.groq_stt import groq_transcribe
from app.services.providers.stt.openai_stt import openai_transcribe
from app.services.providers.stt.gemini_stt import gemini_transcribe


def transcribe_audio(file_path: str) -> str:

    provider = os.getenv("STT_PROVIDER", "groq")

    if provider == "local":
        return local_whisper_transcribe(file_path)

    elif provider == "groq":
        return groq_transcribe(file_path)

    elif provider == "openai":
        return openai_transcribe(file_path)

    elif provider == "gemini":
        return gemini_transcribe(file_path)

    raise ValueError(f"Unknown STT provider: {provider}")