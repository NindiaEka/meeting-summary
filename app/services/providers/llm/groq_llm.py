from langchain_groq import ChatGroq
import os


def get_groq_llm(model_name: str):

    return ChatGroq(
        model=model_name,
        api_key=os.getenv("GROQ_API_KEY"),
        temperature=0
    )