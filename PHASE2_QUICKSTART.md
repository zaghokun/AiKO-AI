# Phase 2 Quick Commands

Fast reference untuk Phase 2 memory system.

---

## 🚀 Start Everything

```powershell
# 1. Start PostgreSQL
docker-compose up -d

# 2. Initialize database (first time only)
cd backend
python scripts/init_db.py

# 3. Start server
python -m app.main
```

---

## 🛑 Stop Everything

```powershell
# Stop server: Ctrl+C in terminal

# Stop PostgreSQL
docker-compose down

# Stop and remove volumes (deletes data!)
docker-compose down -v
```

---

## 🔍 Check Status

```powershell
# Check Docker containers
docker ps

# Check database connection
python -c "from app.database import engine; engine.connect(); print('✅ OK')"

# View logs
docker-compose logs -f postgres
```

---

## 🗄️ Database Commands

```powershell
# Initialize database
python scripts/init_db.py

# Reset database (DELETE ALL!)
python scripts/init_db.py --reset

# Connect to PostgreSQL
docker exec -it aiko_postgres psql -U aiko_user -d aiko_db

# Start pgAdmin
docker-compose --profile tools up -d
# Access: http://localhost:5050
```

---

## 🧪 Testing

```powershell
# Test Gemini API
curl http://localhost:8000/test

# Test chat endpoint
curl -X POST http://localhost:8000/chat -H "Content-Type: application/json" -d '{\"message\": \"Halo Aiko!\"}'

# Get session info
curl http://localhost:8000/session/info?username=default_user

# Get chat history
curl http://localhost:8000/session/history?username=default_user
```

# Test via web
Open: http://localhost:8000/test-chat

---

## 📊 Database Queries

```sql
-- Inside psql (docker exec -it aiko_postgres psql -U aiko_user -d aiko_db)

-- List all tables
\dt

-- View users
SELECT * FROM users;

-- View active sessions
SELECT * FROM chat_sessions WHERE is_active = true;

-- View today's sessions
SELECT * FROM chat_sessions WHERE session_date = CURRENT_DATE;

-- View recent messages
SELECT role, content, timestamp 
FROM messages 
ORDER BY timestamp DESC 
LIMIT 20;

-- Count total messages
SELECT COUNT(*) FROM messages;

-- Messages per session
SELECT session_id, COUNT(*) 
FROM messages 
GROUP BY session_id;

-- Exit psql
\q
```

---

## 🔧 Configuration

Edit `.env`:
```env
# Session duration (hours)
SESSION_DURATION_HOURS=24

# Max messages per session
MAX_MESSAGES_PER_SESSION=100

# Database logging (True for dev, False for prod)
DB_ECHO=False
```

---

## 📦 Dependencies

```powershell
# Install/update dependencies
pip install -r requirements.txt

# Specific packages for Phase 2
pip install sqlalchemy psycopg2-binary alembic python-dateutil
```

---

## 🐛 Quick Fixes

**PostgreSQL not starting?**
```powershell
docker-compose down
docker-compose up -d
```

**Database connection error?**
```powershell
# Check .env has correct DATABASE_URL
# Check PostgreSQL is running: docker ps
```

**Tables don't exist?**
```powershell
python scripts/init_db.py
```

**Want fresh start?**
```powershell
docker-compose down -v  # Remove volumes
docker-compose up -d    # Start fresh
python scripts/init_db.py  # Recreate tables
```

---

## 📁 File Structure (Phase 2)

```
backend/
├── app/
│   ├── database/
│   │   ├── __init__.py
│   │   ├── models.py           # SQLAlchemy models
│   │   ├── connection.py       # DB connection
│   │   └── session_manager.py  # 24h session logic
│   ├── services/
│   │   ├── gemini_service.py
│   │   ├── web_launcher.py
│   │   └── chat_service.py     # NEW: Orchestrates everything
│   ├── config.py               # Updated: DB settings
│   └── main.py                 # Updated: DB integration
├── scripts/
│   └── init_db.py              # Database initialization
├── .env                        # Updated: DB config
└── requirements.txt            # Updated: DB packages

docker-compose.yml              # PostgreSQL + pgAdmin
```

---

**🎯 Most Common Workflow:**

```powershell
# Morning/Start
docker-compose up -d
cd backend
python -m app.main

# Afternoon/Development
# Just code + test in browser

# Evening/Stop
Ctrl+C (stop server)
docker-compose down
```

---

That's it! 🚀
