from langchain_anthropic import ChatAnthropic
import os


def get_anthropic_llm(model_name: str):

    return ChatAnthropic(
        model=model_name,
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        temperature=0
    )