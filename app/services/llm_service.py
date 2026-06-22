import os

from app.services.providers.llm.groq_llm import get_groq_llm
from app.services.providers.llm.openai_llm import get_openai_llm
from app.services.providers.llm.gemini_llm import get_gemini_llm
from app.services.providers.llm.anthropic_llm import get_anthropic_llm


def get_llm(model_name: str):

    provider = os.getenv(
        "LLM_PROVIDER",
        "groq"
    )

    if provider == "groq":
        return get_groq_llm(model_name)

    elif provider == "openai":
        return get_openai_llm(model_name)

    elif provider == "gemini":
        return get_gemini_llm(model_name)

    elif provider == "anthropic":
        return get_anthropic_llm(model_name)

    raise ValueError(
        f"Unknown provider: {provider}"
    )