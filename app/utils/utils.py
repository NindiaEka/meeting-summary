import json
from app.utils.logger import logger


def safe_json_loads(response_text):

    cleaned_response = (
        response_text
        .replace("```json", "")
        .replace("```", "")
        .strip()
    )

    json_start = cleaned_response.find("{")
    json_end = cleaned_response.rfind("}") + 1

    if json_start == -1 or json_end <= 0:

        logger.error(
            "No valid JSON object found."
        )

        return {
            "summary": response_text,
            "key_discussions": [],
            "decisions": [],
            "action_items": []
        }

    cleaned_response = cleaned_response[
        json_start:json_end
    ]

    try:

        return json.loads(cleaned_response)

    except json.JSONDecodeError as e:

        logger.error(
            f"Failed to parse JSON response: {e}"
        )

        logger.error(
            f"Raw response:\n{response_text}"
        )

        logger.error(
            f"Cleaned response:\n{cleaned_response}"
        )

        return {
            "summary": "Failed to parse LLM response",
            "key_discussions": [],
            "decisions": [],
            "action_items": []
        }