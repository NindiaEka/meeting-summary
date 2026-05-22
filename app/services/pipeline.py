from dotenv import load_dotenv
load_dotenv()

from langchain_groq import ChatGroq

from app.services.preprocessing import preprocessing_text
from app.services.chunking import chunk_text
from app.services.aggregation import combine_chunk_summaries
from app.services.speech_to_text import transcribe_audio

from app.utils.utils import safe_json_loads
from app.utils.logger import logger

import os
import time


llm = ChatGroq(
    model=os.getenv("LLM_MODEL"),
    api_key=os.getenv("GROQ_API_KEY"),
)


TEXT_EXTENSIONS = (
    ".txt",
    ".vtt",
    ".srt"
)

AUDIO_EXTENSIONS = (
    ".mp3",
    ".wav",
    ".m4a",
    ".mp4"
)


def process_text(transcript):

    start_time = time.time()

    logger.info(
        "Processing text transcript..."
    )

    cleaned_transcript = preprocessing_text(
        transcript
    )

    chunks = chunk_text(
        cleaned_transcript
    )

    logger.info(
        f"Total chunks: {len(chunks)}"
    )

    all_results = []

    for idx, chunk in enumerate(chunks):

        chunk_start_time = time.time()

        logger.info(
            f"Processing chunk {idx + 1}"
        )

        prompt = f"""
Buatkan Minutes of Meeting dari transcript berikut.

Output wajib JSON valid dengan format:

{{
    "summary": "",
    "key_discussions": [],
    "decisions": [],
    "action_items": []
}}

Gunakan hanya informasi dari transcript.

Transcript:
{chunk}
"""

        logger.info(
            "Sending request to LLM..."
        )

        response = llm.invoke(prompt)

        chunk_end_time = time.time()

        logger.info(
            f"Chunk {idx + 1} processed in "
            f"{chunk_end_time - chunk_start_time:.2f} seconds."
        )

        result = safe_json_loads(
            response.content
        )

        all_results.append(result)

    combined_summary = combine_chunk_summaries(
        all_results
    )

    logger.info(
        "Generating final summary..."
    )

    final_prompt = f"""
Gabungkan hasil summary meeting berikut
menjadi final Minutes of Meeting.

Output wajib JSON valid:

{{
    "summary": "",
    "key_discussions": [],
    "decisions": [],
    "action_items": []
}}

Gabungkan keputusan dan action items
yang muncul pada summary meeting.

Summary Meeting:
{combined_summary}
"""

    final_start_time = time.time()

    final_response = llm.invoke(
        final_prompt
    )

    final_end_time = time.time()

    logger.info(
        f"Final summary generated in "
        f"{final_end_time - final_start_time:.2f} seconds."
    )

    final_result = safe_json_loads(
        final_response.content
    )

    logger.info(
        "Meeting summarization completed."
    )

    end_time = time.time()

    logger.info(
        f"Total processing time: "
        f"{end_time - start_time:.2f} seconds."
    )

    return final_result


def process_meeting(file_path):

    logger.info(
        f"Processing meeting file: {file_path}"
    )

    extension = os.path.splitext(
        file_path
    )[1].lower()

    if extension in AUDIO_EXTENSIONS:

        logger.info(
            "Detected audio file."
        )

        transcript = transcribe_audio(
            file_path
        )

    elif extension in TEXT_EXTENSIONS:

        logger.info(
            "Detected transcript file."
        )

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as f:

            transcript = f.read()

    else:

        raise ValueError(
            "Unsupported file type."
        )

    return process_text(transcript)