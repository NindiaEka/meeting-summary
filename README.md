# Meeting Summary

AI-powered meeting summary automation system using FastAPI, Groq LLM, n8n, and WhatsApp API integration.

---

# Features

- Transcript summarization using LLM
- Audio transcription support
- Structured JSON output
- Chunking & aggregation pipeline
- FastAPI REST API
- Swagger API documentation
- n8n workflow automation
- WhatsApp personal chat delivery
- WhatsApp group delivery
- Docker support
- Logging & error handling

---

# Architecture

```text
Transcript / Audio
↓
FastAPI Backend
↓
AI Processing Pipeline
↓
Aggregation
↓
n8n Workflow
↓
WhatsApp API
↓
WhatsApp Delivery
```

---

# Tech Stack

## Backend
- FastAPI
- Python

## AI / LLM
- Groq API
- Llama 3

## Automation
- n8n

## Messaging
- Baileys WhatsApp API

## Containerization
- Docker

---

# Project Structure

```bash
AI-MoM-Notaker/
│
├── app/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   └── utils/
│
├── input/
├── outputs/
│
├── app.py
├── main.py
├── run_pipeline.py
├── .env
├── pyproject.toml
└── README.md
```

---

# Installation

## Clone Repository

```bash
git clone <repository_url>
cd AI-MoM-Notaker
```

---

# Install Dependencies

Using uv:

```bash
uv sync
```

Or using pip:

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Create `.env` file:

```env
GROQ_API_KEY=your_api_key
LLM_MODEL=llama-3.1-8b-instant
```

---

# Run FastAPI Server

```bash
uv run python main.py
```

API will run on:

```text
http://localhost:8000
```

Swagger documentation:

```text
http://localhost:8000/docs
```

---

# API Endpoint

## POST /summarize

Upload transcript or audio file and generate Minutes of Meeting.

### Supported Transcript
- .txt
- .vtt
- .srt

### Supported Audio
- .mp3
- .wav
- .m4a
- .mp4

---

# Example Response

```json
{
  "summary": "Meeting summary",
  "key_discussions": [
    "Discussion 1"
  ],
  "decisions": [
    "Decision 1"
  ],
  "action_items": [
    "Action item 1"
  ]
}
```

---

# AI Processing Flow

```text
Transcript / Audio
↓
Preprocessing
↓
Chunking
↓
LLM Summarization per chunk
↓
Aggregation
↓
Final Summary
```

---

# n8n Integration

Workflow automation using n8n.

## Workflow

```text
Upload File
↓
AI Summarization
↓
Format Message
↓
Send WhatsApp
```

---

# WhatsApp Integration

Using Baileys-based WhatsApp API Gateway.

## Supported Delivery

### Personal Chat

Input:

```text
628123456789
```

Automatically converted to:

```text
628123456789@s.whatsapp.net
```

---

### Group Chat

Input:

```text
120363403563671925
```

Automatically converted to:

```text
120363403563671925@g.us
```

---

# Docker Support

Example Docker volume mounting:

```bash
-v /host/path:/container/path
```

---

# Logging Features

- Chunk processing
- API request logging
- Processing duration
- Error handling
- Final summary generation

---

# Current Prototype Status

## Completed

- FastAPI integration
- Swagger API
- JSON structured output
- Chunking system
- Aggregation pipeline
- Safe JSON parsing
- n8n integration
- WhatsApp automation
- Docker integration
- Group chat support

---

# Next Development Plan

## Short-term
- Better prompt engineering
- JSON validation
- Async processing
- Database storage

## Mid-term
- Email integration
- Real-time meeting processing
- Multi-language support
- Dashboard monitoring

## Long-term
- Production deployment
- Authentication system
- Queue worker architecture
- Scalable AI processing

---

# Example Workflow

```text
User Upload File
↓
AI MoM Pipeline
↓
Summary Generation
↓
WhatsApp Delivery
```

---



AI MoM Notetaker Prototype Project  
Sisindokom Project
