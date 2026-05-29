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

    all_results = []

    for idx, chunk in enumerate(chunks):

        chunk_start_time = time.time()

        logger.info(
            f"Processing chunk {idx + 1}"
        )

        # UPGRADE PROMPT CHUNK: Memaksa AI mengekstrak detail maksimal per bagian
        prompt = f"""
You are an expert Corporate Secretary. Analyze this transcript chunk and extract highly detailed information for Minutes of Meeting (MoM). Do not oversimplify.

Output MUST be a valid JSON with this exact format (Use professional Indonesian):
{{
    "summary": "Tuliskan ringkasan naratif yang panjang, padat, dan komprehensif dari chunk ini (minimal 1-2 paragraf lengkap). Jelaskan latar belakang dan konteks bisnis dari topik dibahas.",
    "key_discussions": [
        "Detail pembahasan topik A termasuk latar belakang, tantangan teknis/operasional, dan argumen yang muncul",
        "Detail pembahasan topik B termasuk alasan, perbandingan opsi, dan analisis situasi lapangan"
    ],
    "decisions": [
        "Keputusan resmi resmi yang disepakati beserta alasan atau dasar hukum/bisnisnya"
    ],
    "action_items": [
        "Tugas spesifik A [PIC: Tim Terkait/Sebutkan Nama] [Deadline: Sebutkan jika ada/ASAP]",
        "Tugas spesifik B [PIC: Tim Terkait/Sebutkan Nama] [Deadline: Sebutkan jika ada/ASAP]"
    ]
}}

STRICT RULES:
1. Write 100% in professional Indonesian.
2. Provide rich, long, and informative text for each field. Avoid single-word or short bullet points.
3. If PIC or deadline information is not explicitly mentioned, append '[PIC: Akan ditentukan / Tim Terkait]' or '[Deadline: Segera]'.

Transcript Chunk:
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

    # UPGRADE FINAL PROMPT: Konsolidasi total menjadi dokumen MoM eksekutif yang kaya insight
    final_prompt = f"""
You are an expert Project Manager. Consolidate the following meeting summary data into a comprehensive, highly detailed, and professional corporate Minutes of Meeting (MoM). Your goal is to give maximum operational insights to the team.

Output MUST be a valid JSON with this exact format (Use professional Indonesian):
{{
    "summary": "Tuliskan ringkasan eksekutif secara mendalam dan naratif (minimal 2-3 paragraf panjang). Harus mencakup latar belakang pertemuan, tantangan utama yang dibahas (seperti integrasi sistem Singapura-Indonesia, kebutuhan spesifikasi 2 VCPU, migrasi database via PCBU, administrasi SPASPS/SPH/DPG/topner, dan pameran/survei), serta arah strategis perusahaan.",
    "key_discussions": [
        "**Integrasi & Pengembangan API:** Penjelasan detail mengenai rencana menghubungkan Singapura ke Indonesia, urgensi, hambatan teknis, dan arsitekturnya.",
        "**Infrastruktur & Spesifikasi VCPU:** Detail alasan teknis pemilihan spesifikasi 2 VCPU untuk pengembangan sistem baru serta kapasitas performa yang ditargetkan.",
        "**Migrasi Data & Database Baru:** Konteks mendalam mengenai penggunaan PCBU, transisi ke database baru, mitigasi risiko kehilangan data, dan timeline kerja.",
        "**Aspek Komersial, Kontrak & Legalitas:** Penjelasan komprehensif mengenai kontrak BP city, lisensi impor, pemenuhan dokumen SPASPS, SPH (Service Point of Interaction), DPG, dan koordinasi finansial (FI).",
        "**Survei & Strategi Lapangan:** Hasil temuan lapangan mengenai survei target serta persiapan materi presentasi internal ('gua')."
    ],
    "decisions": [
        "Keputusan resmi A yang diambil beserta urgensi atau argumen dasarnya.",
        "Keputusan resmi B terkait infrastruktur/legalitas beserta penjelasannya."
    ],
    "action_items": [
        "[ ] **Pengembangan API Regional:** Tim Dev/PIC wajib menyelesaikan arsitektur API penghubung Singapura-Indonesia termasuk enkripsi data [Target: ASAP/Sebutkan Timeline].",
        "[ ] **Migrasi Data via PCBU:** Tim Data Engineer melakukan uji coba (dry-run) migrasi data ke database baru guna memastikan nol risiko data corrupt [Target: ASAP/Sebutkan Timeline].",
        "[ ] **Finalisasi Dokumen Legal & Lisensi:** Tim Legal/Operasional segera merampungkan administrasi SPASPS, SPH, kontrak BP city, serta kebutuhan lisensi impor [Target: ASAP/Sebutkan Timeline].",
        "[ ] **Survei Lapangan & Dokumentasi:** Tim Terkait menyusun laporan lengkap hasil survei target untuk bahan presentasi final [Target: ASAP/Sebutkan Timeline]."
    ]
}}

STRICT RULES:
1. Do not use short bullet points for the summary or key discussions. Force the AI to output detailed, long, and rich text.
2. Write 100% in professional Indonesian.
3. Keep the JSON keys exactly as requested.

Summary Meeting Data:
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