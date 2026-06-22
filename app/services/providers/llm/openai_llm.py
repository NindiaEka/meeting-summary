from langchain_openai import ChatOpenAI
import os


def get_openai_llm(model_name: str):

    return ChatOpenAI(
        model=model_name,
        api_key=os.getenv("OPENAI_API_KEY"),
        temperature=0
    )