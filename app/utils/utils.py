import json
from app.utils.logger import logger

def safe_json_loads(response_text):
    cleanned_response = (
        response_text.replace("```json", "")
        .replace("```", "")
        .strip()
    )

    json_start = cleanned_response.find("{")
    json_end = (cleanned_response.rfind("}") + 1)

    cleanned_response = cleanned_response[json_start:json_end]

    try:
        return json.loads(cleanned_response)
    except json.JSONDecodeError:
        logger.error("Failed to parse JSON response.")
        return {
            "summary": "Failed to parse LLM response",
            "key_discussions": [],
            "decisions": [],
            "action_items": []
        }