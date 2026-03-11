# Phase 2: Memory System - Setup Guide

Complete guide untuk setup memory system dengan PostgreSQL dan 24-hour session management.

---

## 🎯 Features

- ✅ PostgreSQL database untuk chat history
- ✅ 24-hour session dengan auto-reset (midnight ke midnight)
- ✅ Context-aware conversations (last 20 messages)
- ✅ Message persistence
- ✅ Session information tracking
- ✅ Clean session management

---

## 🚀 Quick Start

### 1. Start PostgreSQL (Docker)

```powershell
# From project root (AiKO-AI/)
docker-compose up -d

# Check if running
docker ps
```

Expected output:
```
CONTAINER ID   IMAGE                  STATUS          PORTS
abc123...      postgres:15-alpine     Up 10 seconds   0.0.0.0:5432->5432/tcp
```

### 2. Update .env File

Copy dari `.env.example` atau tambahkan:

```env
# Database
DATABASE_URL=postgresql://aiko_user:aiko_password_2026@localhost:5432/aiko_db
DB_ECHO=False

# Session
SESSION_DURATION_HOURS=24
MAX_MESSAGES_PER_SESSION=100
```

### 3. Install Dependencies

```powershell
cd backend
pip install -r requirements.txt
```

New packages:
- `sqlalchemy` - ORM
- `psycopg2-binary` - PostgreSQL driver
- `alembic` - Migrations
- `python-dateutil` - Date utilities

### 4. Initialize Database

```powershell
cd backend
python scripts/init_db.py
```

Expected output:
```
✅ Database initialized successfully!

📊 Tables created:
  - users
  - chat_sessions
  - messages
```

### 5. Start Server

```powershell
python -m app.main
```

atau

```powershell
uvicorn app.main:app --reload
```

### 6. Test!

Open: http://localhost:8000/test-chat

Chat dengan Aiko - semua pesan akan tersimpan! 💕

---

## 📊 Database Schema

### Users Table
```sql
users
  - id (uuid, primary key)
  - username (string, unique)
  - created_at (timestamp)
  - updated_at (timestamp)
```

### Chat Sessions Table
```sql
chat_sessions
  - id (uuid, primary key)
  - user_id (uuid, foreign key → users)
  - session_date (date) -- e.g., 2026-03-11
  - started_at (timestamp)
  - expires_at (timestamp) -- 24h from started_at
  - message_count (int)
  - is_active (boolean)
```

### Messages Table
```sql
messages
  - id (uuid, primary key)
  - session_id (uuid, foreign key → chat_sessions)
  - role (string) -- 'user' or 'assistant'
  - content (text)
  - timestamp (timestamp)
  - tokens_used (int, optional)
```

---

## 🔧 How It Works

### Session Lifecycle

1. **User sends first message of the day**
   - System checks for active session
   - If no session or expired → create new session
   - Session date = today's date (2026-03-11)
   - Expires at = now + 24 hours

2. **Subsequent messages**
   - Use existing active session
   - Load last 20 messages as context
   - Save new messages to database

3. **Auto-reset at midnight**
   - Old session becomes inactive
   - New message creates new session
   - Fresh context for new day

4. **Message limit**
   - Default: 100 messages per session
   - Safety limit to prevent abuse
   - Returns friendly message when reached

### Context Management

- Last **20 messages** loaded as context
- Sent to Gemini for conversation continuity
- Recent context = better personality consistency
- Older messages stored but not in active context

---

## 🌐 New API Endpoints

### `POST /chat`
Chat with Aiko (with session management)

**Request:**
```json
{
  "message": "Halo Aiko!",
  "user_id": "default_user"
}
```

**Response:**
```json
{
  "response": "Haii! Apa kabar? 😊",
  "action": null,
  "action_data": {
    "session_id": "abc-123...",
    "session_date": "2026-03-11",
    "message_count": 2,
    "time_remaining_hours": 23.5,
    "is_active": true
  }
}
```

### `GET /session/info?username=default_user`
Get current session information

**Response:**
```json
{
  "status": "success",
  "data": {
    "session_id": "abc-123...",
    "session_date": "2026-03-11",
    "started_at": "2026-03-11T10:30:00",
    "expires_at": "2026-03-12T10:30:00",
    "time_remaining_hours": 23.5,
    "message_count": 10,
    "is_active": true,
    "is_expired": false
  }
}
```

### `GET /session/history?username=default_user&limit=50`
Get chat history for current session

**Response:**
```json
{
  "status": "success",
  "count": 10,
  "messages": [
    {
      "id": "msg-123...",
      "role": "user",
      "content": "Halo Aiko!",
      "timestamp": "2026-03-11T10:30:00"
    },
    {
      "id": "msg-456...",
      "role": "assistant",
      "content": "Haii! Apa kabar? 😊",
      "timestamp": "2026-03-11T10:30:05"
    }
  ]
}
```

---

## 🛠️ Database Management

### View Database (pgAdmin - Optional)

Start pgAdmin:
```powershell
docker-compose --profile tools up -d
```

Access: http://localhost:5050
- Email: `admin@aiko.local`
- Password: `admin123`

Add server:
- Host: `host.docker.internal` (or `aiko_postgres`)
- Port: `5432`
- Database: `aiko_db`
- Username: `aiko_user`
- Password: `aiko_password_2026`

### Reset Database

```powershell
cd backend
python scripts/init_db.py --reset
```

**WARNING:** This deletes ALL data!

### Direct psql Access

```powershell
docker exec -it aiko_postgres psql -U aiko_user -d aiko_db
```

Useful commands:
```sql
-- List tables
\dt

-- View users
SELECT * FROM users;

-- View active sessions
SELECT * FROM chat_sessions WHERE is_active = true;

-- View recent messages
SELECT role, content, timestamp FROM messages ORDER BY timestamp DESC LIMIT 10;

-- Count messages per session
SELECT session_id, COUNT(*) FROM messages GROUP BY session_id;
```

---

## 📈 Session Statistics

View session statistics:

```sql
-- Sessions today
SELECT COUNT(*) FROM chat_sessions 
WHERE session_date = CURRENT_DATE;

-- Total messages today
SELECT SUM(message_count) FROM chat_sessions 
WHERE session_date = CURRENT_DATE;

-- Average messages per session
SELECT AVG(message_count) FROM chat_sessions;
```

---

## 🧹 Cleanup Old Data

The system keeps all sessions by default. To clean up old data:

```python
# In Python shell or script
from app.database import SessionManager, get_db_context

with get_db_context() as db:
    # Delete sessions older than 7 days
    deleted = SessionManager.cleanup_old_sessions(db, days_to_keep=7)
    print(f"Deleted {deleted} old sessions")
```

Consider adding a scheduled task for automatic cleanup.

---

## 🐛 Troubleshooting

### Error: "could not connect to server"

**Fix:** Make sure PostgreSQL is running
```powershell
docker-compose up -d
docker ps  # Should show aiko_postgres running
```

### Error: "relation does not exist"

**Fix:** Initialize database
```powershell
python scripts/init_db.py
```

### Error: "password authentication failed"

**Fix:** Check credentials in `.env` match `docker-compose.yml`

### Messages not persisting

**Fix:** Check database connection
```powershell
# Test database
python -c "from app.database import engine; engine.connect(); print('✅ Connected!')"
```

### Session not resetting after 24h

Session resets when:
1. 24 hours pass from `started_at`
2. User sends a new message
3. System creates new session

Check timezone settings if issues persist.

---

## 📝 Next Steps (Phase 3)

Future enhancements:
- [ ] Multiple users (authentication)
- [ ] Qdrant for RAG (semantic memory)
- [ ] Long-term memory beyond sessions
- [ ] Memory importance scoring
- [ ] Conversation summaries
- [ ] Export chat history

---

## 💡 Tips

1. **Development**: Keep `DB_ECHO=True` to see SQL queries
2. **Production**: Set `DB_ECHO=False` for performance
3. **Backup**: Use `pg_dump` untuk backup database
4. **Monitoring**: Check session counts regularly
5. **Cleanup**: Schedule weekly cleanup of old sessions

---

**Questions?** Check logs or use pgAdmin to inspect database state.

**Ready!** Chat dengan Aiko dan semua conversation akan remembered! 💕🎉
