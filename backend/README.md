# AiKO Backend API

Backend API untuk AiKO - AI Companion dengan personality Aiko (Anjou-style).

## Features
- ✅ Gemini API integration
- ✅ Web launcher (YouTube, Instagram, TikTok, etc)
- ✅ Aiko personality chat
- ✅ Streaming responses
- ✅ CORS enabled

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. COnfigure Environments
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

3. Run Server
```bash
cd backend
python -m app.main
```
Server will run on http://localhost:8000

## API ENDPOINTS
GET /
Health check

POST /chat
Chat with Aiko (with web launcher support)

Request:
```bash
{
  "message": "Halo Aiko!",
  "history": [],
  "user_id": "optional"
}
```

Response
```bash
{
  "response": "Haii! Apa kabar? 😊",
  "action": null,
  "action_data": null
}
```

POST /chat/stream
Streaming chat response (SSE)

GET /test
Test Gemini API connection

Web Launcher
Deteksi otomatis command seperti:

"buka YouTube" → Opens YouTube
"open Instagram" → Opens Instagram
"bukain TikTok dong" → Opens TikTok
Supported websites:

YouTube, Instagram, TikTok, Facebook, Twitter/X
WhatsApp Web, Gmail, Google

## Development
```bash
# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

