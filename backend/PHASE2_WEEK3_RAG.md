# Phase 2 Week 3: RAG System - Setup Guide

Complete guide untuk setup RAG (Retrieval Augmented Generation) dengan Qdrant vector database.

---

## 🎯 What is RAG?

**RAG = Retrieval Augmented Generation**

Sistem yang menggabungkan:
1. **Recent Context** (last 20 messages from PostgreSQL)
2. **Semantic Search** (relevant past conversations from Qdrant)
3. **LLM Generation** (Gemini with enhanced context)

### Example:
```
Day 1:
User: "Aku kemarin interview di startup, tapi gagal"
Aiko: "Aww, rejection emang sakit... Tapi it's okay! Next time pasti lebih baik! 💕"

Day 3 (different session):
User: "Aku mau interview lagi nih"
Aiko: "Oh! Inget ga kemarin kamu cerita gagal interview di startup? 
       Kali ini pasti lebih prepared ya! Aku yakin kamu bisa! 💪✨"
```

↑ **This is possible with RAG!** Aiko remembers conversations from days ago.

---

## 🚀 Quick Setup

### 1. Start Qdrant (Docker)

```powershell
docker-compose up -d
```

This starts:
- PostgreSQL (port 5432)
- Qdrant (port 6333)

Verify:
```powershell
docker ps
# Should show: aiko_postgres, aiko_qdrant, aiko_pgadmin
```

### 2. Install Dependencies

```powershell
cd backend
pip install -r requirements.txt
```

New packages (this will take ~2-5 minutes):
- `qdrant-client` - Vector database client
- `sentence-transformers` - Generate embeddings
- `torch` - ML framework (~1GB download)

**Note:** First run will download embedding model (~80MB)

### 3. Update .env

Add to `backend/.env`:
```env
# Qdrant Vector Database
QDRANT_HOST=localhost
QDRANT_PORT=6333
QDRANT_COLLECTION_NAME=aiko_memories

# RAG Configuration
EMBEDDING_MODEL=all-MiniLM-L6-v2
MEMORY_SEARCH_LIMIT=5
MEMORY_RELEVANCE_THRESHOLD=0.7
```

### 4. Start Server

```powershell
python -m app.main
```

Expected output:
```
🔄 Loading embedding model: all-MiniLM-L6-v2
✅ Embedding model loaded! Dimension: 384
🔄 Creating Qdrant collection: aiko_memories
✅ Collection created!
✅ Database initialized!
INFO:     Uvicorn running on http://0.0.0.0:8000
```

### 5. Test RAG!

Open: http://localhost:8000/test-chat

Try having conversations across multiple days/sessions!

---

## 🧠 How It Works

### Architecture

```
User Message
     ↓
1. Get recent messages (PostgreSQL) → Last 20 messages
2. Search similar memories (Qdrant) → Top 5 relevant past conversations
3. Combine context → Recent + Relevant memories
4. Send to Gemini → Enhanced context for better responses
5. Save new messages → Both PostgreSQL AND Qdrant
```

### Embedding Model

**Model:** `all-MiniLM-L6-v2`
- **Size:** ~80MB
- **Dimension:** 384
- **Speed:** Very fast (~1ms per message)
- **Quality:** Good for semantic search

Each message is converted to a 384-dimensional vector that captures its meaning.

### Similarity Search

Uses **cosine similarity** to find related conversations:
- Score 1.0 = Identical
- Score 0.7+ = Very similar
- Score 0.5-0.7 = Somewhat similar
- Score <0.5 = Not related (filtered out)

---

## 📊 New API Endpoints

### `GET /memory/stats?username=default_user`

Get memory statistics

**Response:**
```json
{
  "status": "success",
  "data": {
    "total_memories": 42,
    "vector_dimension": "all-MiniLM-L6-v2",
    "search_limit": 5,
    "relevance_threshold": 0.7
  }
}
```

### `POST /memory/search`

Search for relevant memories

**Request:**
```json
{
  "query": "interview",
  "username": "default_user",
  "limit": 5
}
```

**Response:**
```json
{
  "status": "success",
  "query": "interview",
  "count": 2,
  "memories": [
    {
      "content": "Aku kemarin interview di startup, tapi gagal",
      "role": "user",
      "timestamp": "2026-03-09T10:30:00",
      "session_id": "abc-123",
      "score": 0.89
    },
    {
      "content": "Aww, rejection emang sakit... Tapi it's okay!",
      "role": "assistant",
      "timestamp": "2026-03-09T10:30:05",
      "session_id": "abc-123",
      "score": 0.75
    }
  ]
}
```

### Updated: `POST /chat`

Now includes RAG memory!

**Response includes:**
```json
{
  "response": "...",
  "memories_used": 3  ← NEW: Number of past memories used
}
```

---

## 🧪 Testing RAG

### Test 1: Basic Memory

```powershell
# Day 1 - Tell Aiko something
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Aku kerja sebagai software engineer di Jakarta"}'

# Later (or simulate new session)
# Stop server, delete session from DB, restart

# Ask related question
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Dimana aku kerja ya?"}'

# Aiko should remember! 🧠
```

### Test 2: Search Memories

```powershell
curl "http://localhost:8000/memory/search?query=pekerjaan&limit=3"
```

### Test 3: Memory Stats

```powershell
curl "http://localhost:8000/memory/stats"
```

---

## 🗄️ Database Structure

### PostgreSQL (Recent Context)
- Stores last 20 messages of current session
- Fast queries
- Structured data

### Qdrant (Long-term Semantic Memory)
- Stores ALL messages as vectors
- Semantic search across ALL past conversations
- Finds similar topics even with different wording

**Example:**
- "gagal interview" similar to "interview tidak berhasil"
- "sedih" similar to "down", "galau"
- "kerja" similar to "pekerjaan", "kantor"

---

## ⚙️ Configuration

### Embedding Model Options

Current: `all-MiniLM-L6-v2` (recommended)

Alternatives:
- `paraphrase-MiniLM-L6-v2` - Better for paraphrasing
- `all-mpnet-base-v2` - Better quality, slower
- `multi-qa-MiniLM-L6-cos-v1` - Better for Q&A

Change in `.env`:
```env
EMBEDDING_MODEL=all-mpnet-base-v2
```

### Memory Search Tuning

```env
# How many past memories to retrieve
MEMORY_SEARCH_LIMIT=5  # Default: 5 (1-10 recommended)

# Minimum similarity score
MEMORY_RELEVANCE_THRESHOLD=0.7  # Default: 0.7 (0.5-0.9 range)
```

**Lower threshold** = More memories (may include less relevant)
**Higher threshold** = Fewer memories (only highly relevant)

---

## 🐛 Troubleshooting

### Error: "Connection refused" (Qdrant)

**Fix:** Make sure Qdrant is running
```powershell
docker-compose up -d
docker logs aiko_qdrant
```

### Error: "Embedding model download failed"

**Fix:** Check internet connection, try again. Model downloads automatically on first run.

### Embeddings taking too long

**Fix:** First message after startup takes longer (model loading). Subsequent messages are fast.

### No memories found

**Fix:** 
1. Have some conversations first (messages are saved to Qdrant)
2. Check threshold isn't too high
3. Verify Qdrant is running: `curl http://localhost:6333/`

### Qdrant UI

Access Qdrant dashboard: http://localhost:6333/dashboard

View collections, points, and search directly!

---

## 📈 Performance

### Embedding Generation
- **Cold start:** ~2-3 seconds (first time, loading model)
- **Warm:** ~10-50ms per message

### Vector Search
- **Search time:** ~5-20ms for 1000 vectors
- **Scales:** Can handle 100K+ vectors easily

### Memory Overhead
- **Embedding model:** ~200MB RAM
- **Qdrant:** ~50MB base + vectors

---

## 🎯 What's Next?

RAG sistem sudah jalan! Now you can:

1. **Test extensively** - Chat across multiple days
2. **Monitor memory** - Check `/memory/stats`
3. **Tune parameters** - Adjust threshold and limit
4. **Move to Phase 3** - Fine-tuning (optional, can skip)
5. **Or Phase 4** - Backend enhancement (auth, WebSocket)
6. **Or Phase 5** - Build proper frontend UI

---

## 💡 Tips

1. **More conversations = Better memory** - System learns from every message
2. **Specific queries work better** - "interview" finds more than "kerja"
3. **Threshold tuning** - Lower if Aiko forgets too much, raise if too much irrelevant memories
4. **Check logs** - Look for "🧠 Found X relevant memories" in console

---

**Ready!** Aiko now has long-term memory! 🧠💕🎉

Questions? Check Qdrant dashboard or memory/stats endpoint!
