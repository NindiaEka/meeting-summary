import re

def preprocessing_text(text):

    # Remove WEBVTT
    text = text.replace("WEBVTT", "")

    # Remove timestamps
    text = re.sub(
        r"(\d{2}:\d{2}:\d{2}\.\d{3}) --> (\d{2}:\d{2}:\d{2}\.\d{3})",
        "",
        text
    )

    # Remove extra newlines and spaces
    text = re.sub(r"\n+", "\n", text)
    text = re.sub(r"\s+", " ", text)
    
    return text.strip()