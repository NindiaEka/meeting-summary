from langchain_google_genai import ChatGoogleGenerativeAI
import os


def get_gemini_llm(model_name: str):

    return ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=os.getenv("GEMINI_API_KEY"),
        temperature=0
    )