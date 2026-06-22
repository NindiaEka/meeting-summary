# AI MoM Notetaker

AI-powered Minutes of Meeting generator built with FastAPI and multiple AI providers.

---

## Features

* Audio and transcript processing
* Speech-to-Text provider abstraction

  * Groq
  * OpenAI
  * Gemini
  * Local Whisper (optional)
* LLM provider abstraction

  * Groq
  * OpenAI
  * Gemini
  * Anthropic
* Automatic text chunking
* Meeting summarization
* Decision extraction
* Action item extraction
* JSON output
* WhatsApp and Email integration via n8n
* Docker support
* Railway deployment

---

# Project Structure

```text
meeting-summary/
│
├── app
│   ├── routers
│   │   └── summarize.py
│   │
│   ├── schemas
│   │
│   ├── services
│   │   ├── aggregation.py
│   │   ├── chunking.py
│   │   ├── llm_service.py
│   │   ├── pipeline.py
│   │   ├── preprocessing.py
│   │   ├── speech_to_text.py
│   │   │
│   │   └── providers
│   │       ├── llm
│   │       │   ├── anthropic_llm.py
│   │       │   ├── gemini_llm.py
│   │       │   ├── groq_llm.py
│   │       │   └── openai_llm.py
│   │       │
│   │       └── stt
│   │           ├── gemini_stt.py
│   │           ├── groq_stt.py
│   │           ├── local_whisper_stt.py
│   │           └── openai_stt.py
│   │
│   ├── utils
│   │   ├── logger.py
│   │   └── utils.py
│   │
│   ├── __init__.py
│   └── app.py
│
├── input
├── outputs
│
├── .env
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── main.py
├── pyproject.toml
├── requirements.txt
├── requirements-local-whisper.txt
├── uv.lock
└── README.md
```

---

# Workflow

```text
Audio / Transcript
        ↓
Preprocessing
        ↓
Chunking
        ↓
Chunk Summary
        ↓
Aggregation
        ↓
Final Summary
        ↓
JSON Output
        ↓
n8n
 ├── WhatsApp
 └── Email
```

---

# Environment Variables

Create a `.env` file:

```env
# STT Provider
# groq | openai | gemini | local
STT_PROVIDER=groq

# API Keys
GROQ_API_KEY=
OPENAI_API_KEY=
GOOGLE_API_KEY=
ANTHROPIC_API_KEY=

# Local Whisper
WHISPER_MODEL=base

# LLM Provider
# groq | openai | gemini | anthropic
LLM_PROVIDER=groq

# Models
CHUNK_MODEL=llama-3.1-8b-instant
FINAL_MODEL=llama-3.3-70b-versatile

# Chunking
CHUNK_SIZE=3000
CHUNK_OVERLAP=200
```

---

# Installation

## Using uv

Install dependencies:

```bash
uv sync
```

Run application:

```bash
uv run main.py
```

Swagger UI:

```text
http://localhost:8000/docs
```

---

# Docker

Build:

```bash
docker compose build
```

Run:

```bash
docker compose up
```

API Documentation:

```text
http://localhost:8000/docs
```

---

# API

## POST /summarize

Supported files:

* `.mp3`
* `.wav`
* `.m4a`
* `.mp4`
* `.txt`
* `.vtt`
* `.srt`

Response:

```json
{
  "summary": "",
  "key_discussions": [],
  "decisions": [],
  "action_items": []
}
```

---

# Supported Providers

## Speech-to-Text

* Groq
* OpenAI
* Gemini
* Local Whisper (optional)

## LLM

* Groq
* OpenAI
* Gemini
* Anthropic

---

# Deployment

Supported platforms:

* Docker
* Railway

Integration:

* n8n
* WhatsApp
* Email

---

# Architecture

```text
Client
   ↓
FastAPI
   ↓
Speech-to-Text Provider
   ↓
Preprocessing
   ↓
Chunking
   ↓
LLM Provider
   ↓
Aggregation
   ↓
JSON Response
   ↓
n8n
 ├── WhatsApp
 └── Email
```

