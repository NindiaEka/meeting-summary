from dotenv import load_dotenv
load_dotenv()

from app.services.llm_service import get_llm

from app.services.preprocessing import preprocessing_text
from app.services.chunking import chunk_text
from app.services.aggregation import combine_chunk_summaries
from app.services.speech_to_text import transcribe_audio

from app.utils.utils import safe_json_loads
from app.utils.logger import logger

import os
import time

TEXT_EXTENSIONS = (
    ".txt",
    ".vtt",
    ".srt"
)

AUDIO_EXTENSIONS = (
    ".mp3",
    ".wav",
    ".m4a",
    ".mpeg",
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

    chunk_llm = get_llm(
        os.getenv("CHUNK_MODEL")
    )

    final_llm = get_llm(
        os.getenv("FINAL_MODEL")
    )

    all_results = []

    for idx, chunk in enumerate(chunks):

        chunk_start_time = time.time()

        logger.info(
            f"Processing chunk {idx + 1}"
        )

        prompt = f"""
You are an expert Corporate Secretary.

Analyze this transcript chunk and extract important information.

Output MUST be valid JSON with this format:

{{
    "summary": "Ringkasan naratif singkat dari bagian ini.",
    "key_discussions": [
        "Topik pembahasan utama"
    ],
    "decisions": [
        "Keputusan yang disepakati"
    ],
    "action_items": [
        "Tugas yang harus dilakukan [PIC] [Deadline]"
    ]
}}

STRICT RULES:

1. Write 100% in professional Indonesian.
2. Do not repeat information.
3. Keep summary concise (maximum 1 paragraph).
4. Maximum 5 key discussions.
5. Maximum 5 decisions.
6. Maximum 5 action items.
7. Return valid JSON only.
8. Do not wrap with ```json.
9. Do not add explanations outside JSON.

Transcript Chunk:

{chunk}
"""

        logger.info(
            "Sending request to LLM..."
        )

        response = chunk_llm.invoke(
            prompt
        )

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

    # UPGRADE FINAL PROMPT: Konsolidasi total menjadi dokumen MoM eksekutif yang kaya insight
    final_prompt = f"""
You are an expert Project Manager.

Combine the following meeting summaries into a professional Minutes of Meeting (MoM).

Output MUST be valid JSON:

{{
    "summary": "Ringkasan eksekutif meeting.",
    "key_discussions": [],
    "decisions": [],
    "action_items": []
}}

STRICT RULES:

1. Write 100% in professional Indonesian.
2. Avoid repeating information.
3. Summary maximum 2 paragraphs.
4. Maximum 10 key discussions.
5. Maximum 10 decisions.
6. Maximum 10 action items.
7. Merge similar items into one.
8. Return valid JSON only.
9. Do not wrap JSON with ```json.
10. Do not add explanations outside JSON.

Summary Meeting Data:

{combined_summary}
"""

    final_start_time = time.time()

    final_response = final_llm.invoke(
        final_prompt
    )

    final_end_time = time.time()

    logger.info(
        f"Final summary generated in "
        f"{final_end_time - final_start_time:.2f} seconds."
    )

    logger.info(final_response.content)
    
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