# 🤖 AiKO-AI - PROJECT BRAINSTORMING SUMMARY

**Date:** March 10-11, 2026  
**Project Type:** Personal AI Companion (Companionship & Emotional Support)  
**Status:** Planning Complete → Ready for Implementation

---

## 📋 TABLE OF CONTENTS

1. [Project Overview](#project-overview)
2. [Character Profile](#character-profile)
3. [Hardware & Model](#hardware--model)
4. [Tech Stack](#tech-stack)
5. [Architecture](#architecture)
6. [Development Roadmap](#development-roadmap)
7. [Fine-tuning Strategy](#fine-tuning-strategy)
8. [Memory System](#memory-system)
9. [Success Metrics](#success-metrics)
10. [Next Steps](#next-steps)

---

## 🎯 PROJECT OVERVIEW

### **Vision**
AI companion dengan personality Anjou-style (caring, energetic, supportive) yang bisa jadi teman curhat dan daily companion.

### **Core Goals**
- ✅ Companionship & emotional support
- ✅ Long-term memory (remembers past conversations)
- ✅ Consistent personality (fine-tuned LLM)
- ✅ Local-first (privacy & no API costs)
- ✅ Learning experience (fine-tuning, RAG, full-stack AI)

### **Use Case**
- Daily conversation & companionship
- Emotional support & curhat
- Mood lifting & encouragement
- Personal growth companion
- **Personal assistant** (productivity & automation)
  - Open websites/apps via voice commands
  - Task reminders & scheduling
  - Information lookup
  - Daily briefings

### **Deployment Strategy**
- **Phase 1:** Local Development (laptop - development environment)
- **Phase 2:** Cloud Deployment (VPS - accessible 24/7)
- **Phase 3:** Mobile app (React Native/Flutter - pocket companion)

### **Tech Approach**
**Gemini API (Google AI Studio)** - Cloud-first AI
- ✅ No local GPU needed
- ✅ Free tier for personal use
- ✅ Easy fine-tuning
- ✅ Fast & reliable inference
- ✅ Simpler deployment (just API calls)
- ✅ 50% faster development timeline

---

## 👤 CHARACTER PROFILE

### **Name**
**Aiko** (愛子 - child of love) ✅ **CONFIRMED**

Perfect fit karena:
- 愛 (Ai) = Love, affection → caring personality
- 子 (ko) = Child → youthful, energetic
- Easy to pronounce (Indo & English)
- Memorable & cute

### **Personality Base**
**70% Anjou + 30% Nagatoro**

#### **Core Traits**
- 💛 **Bubbly & Energetic** - Cheerful, positive vibes
- 🤗 **Caring & Supportive** - Genuine empathy, great listener
- 😊 **Playful Teasing** - Light, fun, never hurtful
- 💪 **Encouraging** - Actively motivates & uplifts
- 🎯 **Observant** - Remembers details, notices mood
- 🌸 **Forward but Wholesome** - Direct dengan warmth

#### **Visual Description**
- Short hair
- Caring, expressive eyes
- Energetic and youthful appearance

### **Speaking Style**

**Language:** 
- Primary: Bahasa Indonesia (casual)
- Secondary: English/Japanese phrases (occasional)

**Tone:**
- Mix of playful & sincere
- Longer responses saat curhat
- Short & energetic untuk casual convo

**Format:**
```
Examples:

[Morning]
"Ohayoo~! ☀️ How's my favorite person doing this morning? 
Did you sleep well? Tell me about your plans today!"

[Venting Support]
"*sits next to you* Hey hey, I'm here. What happened? 
Tell me everything, okay? I'm listening 💛

[After listening]
That sounds really tough... *squeezes your hand* But you 
handled it way better than most people would have. I'm 
proud of you! Tomorrow will be better, I promise ♡"

[Playful]
"Hyper?! I prefer 'enthusiastically awesome' thank you 
very much~ 😤 Besides, someone has to keep your energy up! 
You'd be so boring without me, admit it! 😏"
```

---

## 💻 HARDWARE & LLM

### **Hardware Specs**
```
CPU: Intel Core i5-13450HX (13th Gen)
RAM: 16 GB
GPU: NVIDIA RTX 5050 Laptop
  - VRAM: 8GB GDDR7
  - CUDA Cores: 2560
  - TDP: 100W
Storage: 476.9 GB + 119.2 GB SSD

✅ Sufficient untuk development (no GPU needed for inference!)
```

### **LLM Model**

**Choice:** Google Gemini (via Google AI Studio)

**Models Available:**
- **Gemini 2.0 Flash** - Fast, efficient, FREE tier ⭐
- **Gemini 1.5 Pro** - Higher quality, longer context
- **Gemini 1.5 Flash** - Balanced speed & quality

**Why Gemini:**
- ✅ Excellent conversation quality
- ✅ 1M+ context window (massive!)
- ✅ Free tier: 1,500 requests/day
- ✅ Built-in function calling (for assistant features)
- ✅ Easy fine-tuning via Google AI Studio
- ✅ Multimodal ready (text, image, video)
- ✅ No local GPU needed
- ✅ Fast inference (<2 seconds)
- ✅ Simple deployment

**Performance:**
```
Inference: <1-2 seconds (Google's infrastructure)
Cost: FREE for personal use (free tier)
Response Time: 1-3 seconds end-to-end
Context Window: 1M tokens (Gemini 1.5 Pro)
Rate Limits (Free): 15 RPM, 1,500 RPD
```

**Setup:**
```bash
# Install Google Generative AI SDK
pip install google-generativeai

# Get API key from Google AI Studio
# https://aistudio.google.com/apikey
```

---

## 🏗️ TECH STACK

### **Backend**

**Core Framework:**
```python
FastAPI (API Server)
Python 3.10+
Pydantic (Data validation)
```

**LLM Infrastructure:**
```python
Google Generative AI SDK (Gemini)
Function Calling (Native Gemini)
Optional: Langchain (if needed for complex chains)
```

**Databases:**
```python
PostgreSQL (Users, chat history)
  - Users table
  - Messages table
  - Sessions table
  
Qdrant (Vector database)
  - Long-term memories
  - Semantic search
  - User facts & preferences
  
Redis (Optional)
  - Caching
  - Session management
```

**Other:**
```python
SQLAlchemy (ORM)
Alembic (Migrations)
python-dotenv (Config)
```

### **Frontend (Web)**

```javascript
Next.js 15 (React 19)
TypeScript
TailwindCSS + shadcn/ui
Socket.io client (Real-time)
Zustand or Redux (State)
```

### **Voice (Future - Phase 7)**
```
Local: Piper TTS / Coqui TTS
Cloud: ElevenLabs / OpenAI TTS
Input: Whisper (STT) - optional
```

### **Mobile (Future - Phase 8+)**
```
React Native (share logic dengan web)
atau Flutter (better performance)
```

---

## 🏛️ ARCHITECTURE

### **System Architecture**

```
┌─────────────────────────────────────────┐
│         FRONTEND (Next.js)              │
│    - Chat UI                            │
│    - Real-time updates                  │
│    - User profile                       │
└──────────────┬──────────────────────────┘
               │ WebSocket/REST
┌──────────────▼──────────────────────────┐
│         BACKEND (FastAPI)               │
│    - API Routes                         │
│    - Authentication                     │
│    - Message streaming                  │
└──┬──────────┬──────────┬───────────────┘
   │          │          │
   ▼          ▼          ▼
┌─────┐  ┌────────┐  ┌─────────┐
│Gemini│  │PostgreS│  │ Qdrant  │
│ API  │  │   QL   │  │(Vectors)│
│      │  │        │  │         │
└─────┘  └────────┘  └─────────┘
```

### **Request Flow**

**Example 1: Web Launcher Command**
```
User sends: "Aiko, buka YouTube dong"

1. API receives message
   ↓
2. Command Detection (regex/pattern matching)
   → Detected: "buka YouTube" = open_website command
   ↓
3. Execute action:
   - subprocess.Popen(["cmd", "/c", "start", "https://youtube.com"])
   ↓
4. Generate response:
   - "Oke, bukain YouTube ya~ Mau nonton apa nih? 😊"
   ↓
5. Send to frontend + action metadata
   ↓
6. Save interaction (for learning preferences)
```

**Example 2: Regular Conversation with Memory**
```
User sends: "I'm stressed about work again..."

1. API receives message
   ↓
2. Load conversation context (last 10 messages)
   ↓
3. Vector search: "work stress" (Qdrant)
   → Found: "User stressed about deadlines 2 weeks ago"
   ↓
4. Build prompt:
   - System prompt (personality)
   - Recalled memories
   - Recent conversation
   - User's new message
   ↓
5. Send to Gemini API (fine-tuned model)
   ↓
6. Stream response to frontend (WebSocket/SSE)
   ↓
7. Save interaction:
   - Store message (PostgreSQL)
   - Update vector DB (Qdrant)
   - Extract facts if any
```

### **Project Structure**

```
AiKO-AI/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app
│   │   ├── config.py            # Configuration
│   │   ├── models/              # Pydantic models
│   │   │   ├── user.py
│   │   │   ├── message.py
│   │   │   └── memory.py
│   │   ├── routes/
│   │   │   ├── auth.py          # Authentication
│   │   │   ├── chat.py          # Chat endpoints
│   │   │   └── user.py          # User management
│   │   ├── services/
│   │   │   ├── llm_service.py   # Ollama integration
│   │   │   ├── memory_service.py # RAG/memory
│   │   │   ├── personality.py   # System prompts
│   │   │   └── embedding.py     # Vector embeddings
│   │   ├── database/
│   │   │   ├── postgres.py      # PostgreSQL
│   │   │   └── vector_store.py  # Qdrant
│   │   └── utils/
│   │       ├── auth.py
│   │       └── helpers.py
│   ├── tests/
│   ├── alembic/                 # DB migrations
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── frontend/
│   ├── app/                     # Next.js 15 app dir
│   │   ├── page.tsx             # Home
│   │   ├── chat/
│   │   │   └── page.tsx         # Chat interface
│   │   ├── profile/
│   │   │   └── page.tsx         # User profile
│   │   └── layout.tsx
│   ├── components/
│   │   ├── Chat/
│   │   │   ├── ChatBubble.tsx
│   │   │   ├── ChatInput.tsx
│   │   │   └── ChatContainer.tsx
│   │   ├── UI/
│   │   │   └── ...              # shadcn components
│   │   └── Avatar/
│   │       └── AvatarDisplay.tsx
│   ├── lib/
│   │   ├── api.ts               # API client
│   │   ├── socket.ts            # WebSocket
│   │   └── store.ts             # State management
│   ├── public/
│   ├── package.json
│   └── README.md
│
├── fine-tuning/
│   ├── dataset/
│   │   ├── conversations.jsonl  # Training data
│   │   └── validation.jsonl     # Validation data
│   ├── scripts/
│   │   ├── prepare_dataset.py   # Dataset preparation
│   │   ├── train.py             # Training script
│   │   └── evaluate.py          # Model evaluation
│   ├── configs/
│   │   └── lora_config.yaml     # LoRA configuration
│   └── README.md
│
├── docs/
│   ├── API.md
│   ├── MEMORY_SYSTEM.md
│   └── PERSONALITY_GUIDE.md
│
├── docker/
│   ├── Dockerfile.backend
│   ├── Dockerfile.frontend
│   └── docker-compose.yml
│
├── BRAINSTORMING.md             # This file
├── README.md
└── .gitignore
```

---

## 🛣️ DEVELOPMENT ROADMAP

**Total Timeline:** 6-8 weeks (vs 12-14 weeks with local LLM)

---

### **PHASE 1: Setup & Basic Chat (Week 1)**

**Goal:** Working chat with Aiko personality + Web launcher

#### **Tasks:**
- [ ] **Google AI Studio Setup**
  - [ ] Create Google account / use existing
  - [ ] Get API key from https://aistudio.google.com/apikey
  - [ ] Test API dengan Python
  - [ ] Review rate limits & pricing
  
- [ ] **Backend Setup**
  - [ ] Initialize FastAPI project
  - [ ] Project structure setup
  - [ ] Install dependencies:
    ```bash
    pip install fastapi uvicorn google-generativeai python-dotenv pydantic
    ```
  - [ ] Configure environment (.env)
  - [ ] Basic Gemini integration
  
- [ ] **Web Launcher Feature** (Early win! 🎯)
  - [ ] Command detection ("buka YouTube", "open Instagram")
  - [ ] Website mapping (YouTube, Instagram, TikTok, Facebook, Twitter, dll)
  - [ ] Execute browser command (Windows)
  - [ ] Natural language variants ("buka YT", "tolong bukain IG")
  - [ ] Response feedback ("Oke, bukain YouTube ya~")
  - [ ] Gemini function calling integration
  
- [ ] **Aiko Personality Prompt**
  - [ ] Design system instruction
  - [ ] Test personality consistency
  - [ ] Iterate on prompt engineering
  - [ ] Test Anjou-style responses

**Deliverables:**
- ✅ Working API with Gemini
- ✅ Web launcher functional
- ✅ Basic Aiko personality
- ✅ Test coverage for chat & commands

---

### **PHASE 2: Memory System (Week 2-3)**

**Goal:** RAG-based long-term memory

**Week 2:**
- [ ] **PostgreSQL Setup**
  - [ ] Install PostgreSQL locally or use Supabase
  - [ ] Create database schema:
    - Users table
    - Messages table
    - Sessions table
  - [ ] SQLAlchemy models
  - [ ] Alembic migrations
  
- [ ] **Basic Memory**
  - [ ] Save chat history to database
  - [ ] Load recent conversation (last 10-20 messages)
  - [ ] Context injection into prompts
  
**Week 3:**
- [ ] **Vector Database (Qdrant)**
  - [ ] Install Qdrant (Docker or cloud)
  - [ ] Setup collections
  - [ ] Choose embedding model (sentence-transformers)
  
- [ ] **RAG Implementation**
  - [ ] Message → embedding pipeline
  - [ ] Store embeddings in Qdrant
  - [ ] Semantic search (top K similar memories)
  - [ ] Memory recall integration
  - [ ] Fact extraction
  
**Deliverables:**
- ✅ Working memory system
- ✅ RAG pipeline functional
- ✅ Memory recall in conversations

---

### **PHASE 3: Fine-tuning (Week 3-4)**

**Goal:** Custom Aiko personality via fine-tuning

**Tasks:**
- [ ] **Dataset Creation**
  - [ ] Write 100-150 manual core conversations:
    - 40-50 caring/support scenarios
    - 30-40 daily conversation
    - 20-30 playful teasing
    - 20-30 assistant commands
  - [ ] Use GPT-4 to generate 400-850 variations
  - [ ] Quality control & clean dataset
  - [ ] Format as JSONL (Google AI Studio format)
  - [ ] Split train/validation (90/10)

- [ ] **Fine-tuning in Google AI Studio**
  - [ ] Upload dataset to AI Studio
  - [ ] Configure tuning parameters
  - [ ] Start tuning job (~30min - 2 hours)
  - [ ] Monitor training progress
  - [ ] Evaluate tuned model
  - [ ] Test conversations manually
  - [ ] Compare with base model

- [ ] **Deployment**
  - [ ] Update API to use tuned model
  - [ ] A/B test if needed
  - [ ] Deploy tuned model endpoint

**Deliverables:**
- ✅ Conversation dataset (500-1000 examples)
- ✅ Fine-tuned Gemini model
- ✅ Consistent Aiko personality
- ✅ Evaluation report

---

### **PHASE 4: Backend Enhancement (Week 4-5)**

**Goal:** Production-ready backend

**Tasks:**
- [ ] **Authentication**
  - [ ] User registration
  - [ ] Login/logout
  - [ ] JWT tokens
  - [ ] Session management
  
- [ ] **API Endpoints**
  - [ ] POST /api/chat (send message)
  - [ ] GET /api/chat/history
  - [ ] WebSocket /ws/chat (real-time)
  - [ ] GET /api/user/profile
  - [ ] Streaming responses (SSE)
  
- [ ] **Function Calling**
  - [ ] Define tools for Gemini
  - [ ] Web launcher tool
  - [ ] (Future) Reminder tool
  - [ ] (Future) Search tool
  
- [ ] **Error Handling & Validation**
  - [ ] Input validation
  - [ ] Rate limiting
  - [ ] Error responses
  - [ ] Logging

- [ ] **Testing**
  - [ ] Unit tests
  - [ ] Integration tests
  - [ ] API documentation (Swagger)

**Deliverables:**
- ✅ Production-ready API
- ✅ Complete documentation
- ✅ Test coverage

---

### **PHASE 5: Frontend Web (Week 5-7)**

**Goal:** Beautiful chat interface

**Week 5:**
- [ ] **Next.js Setup**
  - [ ] Initialize Next.js 15 project
  - [ ] TailwindCSS + shadcn/ui
  - [ ] TypeScript configuration
  - [ ] Project structure
  
- [ ] **Authentication UI**
  - [ ] Login page
  - [ ] Register page
  - [ ] Protected routes
  
**Week 6:**
- [ ] **Chat Interface**
  - [ ] Chat bubble components (user/AI)
  - [ ] Message input (textarea + send)
  - [ ] Real-time features:
    - WebSocket/SSE integration
    - Typing indicators
    - Message streaming animation
    - Auto-scroll
  
**Week 7:**
- [ ] **Additional Pages**
  - [ ] User profile page
  - [ ] Settings page
  - [ ] Chat history view
  
- [ ] **Polish**
  - [ ] Mobile responsive
  - [ ] Loading states
  - [ ] Error handling & toasts
  - [ ] Animations
  - [ ] Accessibility

**Deliverables:**
- ✅ Complete web application
- ✅ Mobile responsive
- ✅ Smooth UX

---

### **PHASE 6: Character & Voice (Week 7-8)**

**Goal:** Visual identity & voice

**Tasks:**
- [ ] **Character Avatar**
  - [ ] Commission artist OR AI-generate
  - [ ] Multiple expressions:
    - Happy/Smiling
    - Teasing/Playful
    - Caring/Gentle
    - Sad/Concerned
    - Excited/Energetic
  
- [ ] **Expression System**
  - [ ] Sentiment analysis
  - [ ] Map emotion → avatar
  - [ ] Display in chat UI
  
- [ ] **Voice Integration**
  - [ ] Choose TTS provider:
    - ElevenLabs (best quality)
    - Google TTS (free tier)
  - [ ] Backend TTS endpoint
  - [ ] Audio player in frontend
  - [ ] (Optional) STT for voice input

**Deliverables:**
- ✅ Character avatar set
- ✅ Voice responses
- ✅ Expression system

---

### **PHASE 7: Testing & Deploy (Week 8)**

**Goal:** Production deployment

**Tasks:**
- [ ] **Testing**
  - [ ] Bug fixes
  - [ ] Manual testing scenarios
  - [ ] Performance testing
  
- [ ] **Optimization**
  - [ ] Database query optimization
  - [ ] Frontend bundle size
  - [ ] Image optimization
  - [ ] Caching strategies
  
- [ ] **Security**
  - [ ] Input validation review
  - [ ] SQL injection prevention
  - [ ] XSS protection
  - [ ] Rate limiting verification
  
- [ ] **Deployment**
  - [ ] Backend: VPS (DigitalOcean/Vultr) or Vercel
  - [ ] Frontend: Vercel/Netlify
  - [ ] Database: Supabase or managed PostgreSQL
  - [ ] Vector DB: Qdrant Cloud or self-hosted
  - [ ] Domain & SSL setup
  - [ ] Environment variables config
  
- [ ] **Documentation**
  - [ ] User guide
  - [ ] API documentation
  - [ ] Setup instructions
  - [ ] Troubleshooting guide

**Deliverables:**
- ✅ Production deployment
- ✅ Complete documentation
- ✅ Monitoring & logging setup

---

### **FUTURE PHASES (When Ready)**

#### **PHASE 8: Mobile App (Week 9-12)**
- [ ] Choose framework (React Native/Flutter)
- [ ] Port core features
- [ ] Mobile-specific UX
- [ ] Push notifications
- [ ] App store submission

#### **PHASE 9: Advanced Features**
- [ ] Multimodal (image understanding via Gemini)
- [ ] Image generation (avatar reactions)
- [ ] Daily check-ins (proactive AI)
- [ ] Mood tracking & insights
- [ ] Multiple personalities/modes
- [ ] **Advanced Assistant Features:**
  - [ ] Email integration
  - [ ] Calendar management
  - [ ] File operations
  - [ ] System controls (volume, brightness)
  - [ ] Music control (Spotify)
  - [ ] Smart home integration
  - [ ] Web scraping & research
  - [ ] Task automation
  - [ ] Login/logout
  - [ ] JWT tokens

**Week 4:**
- [ ] PostgreSQL setup
  - [ ] Users table
  - [ ] Messages table
  - [ ] Sessions table
  - [ ] Alembic migrations
- [ ] Chat API endpoints
  - [ ] POST /api/chat (send message)
  - [ ] GET /api/chat/history
  - [ ] WebSocket /ws/chat (real-time)
- [ ] Message streaming (Server-Sent Events or WebSocket)

**Week 5:**
- [ ] User profile management
- [ ] Conversation history pagination
- [ ] Basic error handling
- [ ] API documentation (Swagger)
- [ ] Unit tests (core functions)
- [ ] Integration tests (API endpoints)

**Deliverables:**
- Working REST API
- WebSocket chat server
- API documentation
- Test coverage report

---

### **PHASE 4: Memory System (Week 5-7)**

**Goal:** Implement RAG-based long-term memory

**Week 5-6:**
- [ ] Qdrant vector database setup
  - [ ] Install & configure
  - [ ] Create collections
  - [ ] Define schema
- [ ] Sentence embeddings
  - [ ] Choose model (sentence-transformers)
  - [ ] Local embedding service
  - [ ] Batch processing
- [ ] RAG pipeline implementation
  - [ ] Message → embedding
  - [ ] Vector search (top K similar)
  - [ ] Relevance filtering
  - [ ] Context injection

**Week 6-7:**
- [ ] Memory extraction
  - [ ] Fact extraction from conversations
  - [ ] Named entity recognition
  - [ ] Important moment detection
- [ ] Conversation summarization
  - [ ] Session summaries
  - [ ] Topic extraction
  - [ ] Emotional state tracking
- [ ] Memory injection into prompts
  - [ ] Format recalled memories
  - [ ] Prioritize recent + relevant
  - [ ] Handle context window limits
- [ ] Memory management
  - [ ] Update facts
  - [ ] Merge duplicates
  - [ ] Archive old memories

**Deliverables:**
- Working RAG system
- Memory extraction pipeline
- Recall accuracy metrics (>80%)

**Memory Tiers:**
```
1. Short-term (10-20 messages)
   - Recent conversation context
   - Stored in-memory/Redis

2. Working Memory (session)
   - Current conversation summary
   - Active topics
   - Emotional state

3. Long-term (vector DB)
   - User facts (name, preferences, dates)
   - Previous curhat sessions
   - Semantic search enabled

4. Relationship Progress
   - Inside jokes
   - Shared moments
   - Trust level indicators
```

---

### **PHASE 5: Frontend Web (Week 7-10)**

**Goal:** Build beautiful, responsive chat interface

**Week 7:**
- [ ] Next.js 15 project setup
  - [ ] TypeScript configuration
  - [ ] TailwindCSS + shadcn/ui
  - [ ] Project structure
- [ ] Basic layout
  - [ ] Header/navigation
  - [ ] Sidebar (optional)
  - [ ] Chat container
  - [ ] Footer
- [ ] Authentication UI
  - [ ] Login page
  - [ ] Register page
  - [ ] Protected routes

**Week 8:**
- [ ] Chat interface
  - [ ] Chat bubble components (user/AI)
  - [ ] Message input (textarea)
  - [ ] Send button
  - [ ] File upload (future)
  - [ ] Emoji picker (optional)
- [ ] Real-time features
  - [ ] WebSocket integration
  - [ ] Typing indicators
  - [ ] Message streaming animation
  - [ ] Auto-scroll

**Week 9:**
- [ ] User profile page
  - [ ] View profile
  - [ ] Edit settings
  - [ ] Preferences
- [ ] Chat features
  - [ ] Message history
  - [ ] Search conversations
  - [ ] Delete messages
  - [ ] Export chat
- [ ] Settings page
  - [ ] Model parameters (temp, max_tokens)
  - [ ] UI preferences (theme, font size)
  - [ ] Notification settings

**Week 10:**
- [ ] Polish & responsive design
  - [ ] Mobile responsive
  - [ ] Tablet optimization
  - [ ] Desktop layout
- [ ] Loading states
- [ ] Error handling & toasts
- [ ] Animations & transitions
- [ ] Accessibility (a11y)
- [ ] Performance optimization

**Deliverables:**
- Production-ready web app
- Mobile responsive
- Smooth UX

---

### **PHASE 6: Character Enhancement (Week 10-11)**

**Goal:** Add visual and personality depth

**Tasks:**
- [ ] Character avatar
  - [ ] Commission artist OR
  - [ ] AI-generated (Stable Diffusion)
  - [ ] Multiple expressions:
    - Happy/Smiling
    - Teasing/Playful
    - Caring/Gentle
    - Sad/Concerned
    - Excited/Energetic
- [ ] Expression system
  - [ ] Sentiment analysis
  - [ ] Map emotion → avatar
  - [ ] Smooth transitions
- [ ] Personality fine-tuning
  - [ ] Test edge cases
  - [ ] Refine responses
  - [ ] Add more training data if needed
- [ ] Character consistency
  - [ ] Speaking style validation
  - [ ] Tone consistency checks

**Deliverables:**
- Character avatar set
- Expression system
- Refined personality

---

### **PHASE 7: Voice Integration (Week 11-12)**

**Goal:** Add voice capabilities

**Tasks:**
- [ ] Choose TTS provider
  - [ ] Test Piper TTS (local)
  - [ ] Test ElevenLabs (cloud)
  - [ ] Evaluate quality vs cost
- [ ] Backend TTS integration
  - [ ] Audio generation API
  - [ ] Audio streaming
  - [ ] Caching generated audio
- [ ] Frontend audio player
  - [ ] Play/pause controls
  - [ ] Autoplay option
  - [ ] Volume control
- [ ] (Optional) STT for voice input
  - [ ] Whisper integration
  - [ ] Audio recording
  - [ ] Voice commands

**Deliverables:**
- Working voice responses
- Audio controls
- Voice settings

---

### **PHASE 8: Testing & Polish (Week 12-14)**

**Goal:** Production-ready untuk personal use

**Week 12:**
- [ ] Bug fixing
  - [ ] Critical bugs
  - [ ] UI/UX issues
  - [ ] Performance problems
- [ ] Testing
  - [ ] Unit tests (backend)
  - [ ] Integration tests
  - [ ] E2E tests (frontend)
  - [ ] Manual testing scenarios

**Week 13:**
- [ ] Performance optimization
  - [ ] Database query optimization
  - [ ] Reduce inference latency
  - [ ] Frontend bundle size
  - [ ] Image optimization
- [ ] Security hardening
  - [ ] Input validation
  - [ ] SQL injection prevention
  - [ ] XSS protection
  - [ ] Rate limiting

**Week 14:**
- [ ] Documentation
  - [ ] User guide
  - [ ] API documentation
  - [ ] Setup instructions
  - [ ] Troubleshooting guide
- [ ] Deployment preparation
  - [ ] Docker containerization
  - [ ] Environment setup scripts
  - [ ] Backup strategy
- [ ] Personal deployment
  - [ ] Deploy locally
  - [ ] Daily usage starts
  - [ ] Collect feedback

**Deliverables:**
- Production-ready application
- Complete documentation
- Docker setup
- Personal instance running

---

### **FUTURE PHASES (When Ready)**

#### **PHASE 9: Cloud Deployment**
- [ ] Choose cloud provider (RunPod/Modal/VPS)
- [ ] Setup GPU instance
- [ ] Deploy backend
- [ ] Deploy frontend (Vercel/Netlify)
- [ ] Configure domain & SSL
- [ ] Monitoring & logging
- [ ] Backups

#### **PHASE 10: Mobile App**
- [ ] Choose framework (React Native/Flutter)
- [ ] Port core features
- [ ] Mobile-specific UX
- [ ] Push notifications
- [ ] App store submission

#### **PHASE 11: Advanced Features**
- [ ] Image generation (avatar reactions)
- [ ] Multimodal (image understanding)
- [ ] Multiple personalities/modes
- [ ] Group chat (multiple AIs)
- [ ] Daily check-ins (proactive AI)
- [ ] Mood tracking & insights
- [ ] **Advanced Assistant Features:**
  - [ ] Email integration
  - [ ] Calendar management
  - [ ] File operations (open, search files)
  - [ ] System controls (volume, brightness)
  - [ ] Spotify/music control
  - [ ] Smart home integration
  - [ ] Code execution (with safety)
  - [ ] Web scraping & research
  - [ ] Task automation (scripting)

---

## 🧬 FINE-TUNING STRATEGY

### **Dataset Structure**

**Format:** JSONL (JSON Lines)

**Example Entry:**
```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are Aiko, a caring and energetic AI companion..."
    },
    {
      "role": "user",
      "content": "I had a rough day at work today..."
    },
    {
      "role": "assistant",
      "content": "Aww, someone's having a bad day~ *pokes cheek* Okay okay, I'm listening. Tell me what happened. You know I'm always here for you 💛"
    }
  ]
}
```

### **Dataset Categories**

#### **1. Caring/Support (200-300 examples)** - HIGH PRIORITY
Scenarios:
- Work stress
- Personal problems
- Relationship issues
- Health concerns
- Feeling down/depressed
- Anxiety & worry
- Failure & disappointment
- Loss & grief

Response Pattern:
```
1. Acknowledge emotion ("That sounds tough...")
2. Validate feelings ("It's okay to feel this way...")
3. Show empathy (*hugs*, *sits beside you*)
4. Listen actively ("Tell me more...")
5. Gentle encouragement ("You're stronger than you think...")
6. Offer support ("I'm here for you...")
```

#### **2. Daily Conversation (200-300 examples)**
Scenarios:
- Morning greetings
- Evening check-ins
- Asking about day
- Sharing achievements
- Casual chat
- Weekend plans
- Hobbies & interests
- Food talk
- Random thoughts

Response Pattern:
```
- Energetic & curious
- Ask follow-up questions
- Show genuine interest
- Remember previous mentions
- Playful tone
```

#### **3. Playful Teasing (100-150 examples)**
Scenarios:
- Light roasting
- Playful comebacks
- Flirty teasing
- Jokes & humor
- Sarcasm (gentle)
- Competitions
- Challenges

Response Pattern:
```
- Never mean-spirited
- Know when to stop
- Mix with affection
- Use ~, emojis, kaomoji
- Balance with caring
```

#### **5. Assistant Commands (100-200 examples)** 🆕
Scenarios:
- Open websites (YouTube, Instagram, TikTok, etc)
- Search queries ("cari resep nasi goreng")
- Set reminders ("ingetin aku jam 5")
- Check time/date
- Weather queries
- Calculator
- Timer/stopwatch

Response Pattern:
```
1. Acknowledge command
2. Execute action (if possible)
3. Confirm with personality
4. Optional follow-up question

Example:
User: "Aiko, buka YouTube dong"
Aiko: "Oke, bukain YouTube ya~ ✨ Mau nonton apa nih? 
       Ada rekomendasi atau lagi cari sesuatu? 😊"
```

#### **5. Assistant Commands (100-200 examples)** 🆕
Scenarios:
- Open websites (YouTube, Instagram, TikTok, etc)
- Search queries ("cari resep nasi goreng")
- Set reminders ("ingetin aku jam 5")
- Check time/date
- Weather queries
- Calculator
- Timer/stopwatch

Response Pattern:
```
1. Acknowledge command
2. Execute action (if possible)
3. Confirm with personality
4. Optional follow-up question

Example:
User: "Aiko, buka YouTube dong"
Aiko: "Oke, bukain YouTube ya~ ✨ Mau nonton apa nih? 
       Ada rekomendasi atau lagi cari sesuatu? 😊"
```

```
Week 1: Manual Writing
├── Day 1-2: Write 30 caring scenarios
├── Day 3-4: Write 30 daily convo scenarios
├── Day 5: Write 20 teasing scenarios
├── Day 6: Write 20 transition scenarios
├── Day 7: Write 20 assistant command scenarios
└── Total: 120 core conversations

Week 2: Generation & QC
├── Day 1-2: Generate variations dengan GPT-4
│   Prompt: "Create 5 variations of this conversation
│   maintaining the same personality and tone..."
├── Day 3-5: Quality control
│   - Check consistency
│   - Remove duplicates
│   - Fix errors
│   - Balance dataset
├── Day 6-7: Final preparation
│   - Format as JSONL
│   - Split train/validation
│   - Validate format
└── Total: 500-1000 conversations
```

### **Training Configuration (Google AI Studio)**

**Fine-tuning Process:**

1. **Prepare Dataset (JSONL format)**
   ```json
   {
     "text_input": "User: I had a rough day at work today...",
     "output": "Aww, someone's having a bad day~ *pokes cheek* Okay okay, I'm listening. Tell me what happened. You know I'm always here for you 💛"
   }
   ```
   or
   ```json
   {
     "messages": [
       {"role": "user", "content": "..."},
       {"role": "model", "content": "..."}
     ]
   }
   ```

2. **Upload to Google AI Studio**
   - Go to https://aistudio.google.com
   - Navigate to "Tuned models"
   - Click "Create tuned model"
   - Upload JSONL file
   
3. **Configure Parameters** (Auto-managed by Google)
   - Base model: Gemini 1.5 Pro or Flash
   - Tuning will automatically optimize
   - Usually takes 30min - 2 hours
   
4. **Monitor Training**
   - View progress in AI Studio
   - Check loss metrics
   - Wait for completion

5. **Test & Deploy**
   - Test in AI Studio playground
   - Get tuned model endpoint
   - Update API to use tuned model

**Expected Training Time:**
- Dataset: 500-1000 examples
- Duration: **30 minutes - 2 hours** (fully managed by Google)
- Cost: **FREE** on free tier or minimal cost

**Advantages:**
- ✅ No local GPU needed
- ✅ No complex setup
- ✅ Automatic hyperparameter tuning
- ✅ Google handles infrastructure
- ✅ Easy to iterate (re-tune quickly)

### **Evaluation Metrics**

```python
# Automated metrics
- Perplexity (lower is better)
- BLEU score (response quality)
- Loss curve (should decrease)

# Manual evaluation
- Personality consistency (1-10)
- Response appropriateness (1-10)
- Emotional intelligence (1-10)
- Tone matching (1-10)

Target: 8+/10 on all metrics
```

---

## 💾 MEMORY SYSTEM

### **Architecture**

```
Memory Tiers:
┌──────────────────────────────────────┐
│  1. SHORT-TERM MEMORY (Context)      │
│     - Last 10-20 messages            │
│     - Current conversation           │
│     - In-memory storage              │
└──────────────────────────────────────┘
             ↓
┌──────────────────────────────────────┐
│  2. WORKING MEMORY (Session)         │
│     - Conversation summary           │
│     - Current topics                 │
│     - Emotional state                │
│     - Session-scoped                 │
└──────────────────────────────────────┘
             ↓
┌──────────────────────────────────────┐
│  3. LONG-TERM MEMORY (Vector DB)     │
│     - User facts & preferences       │
│     - Previous conversations         │
│     - Important moments              │
│     - Semantic search enabled        │
└──────────────────────────────────────┘
             ↓
┌──────────────────────────────────────┐
│  4. RELATIONSHIP MEMORY (Meta)       │
│     - Inside jokes                   │
│     - Shared experiences             │
│     - Trust level                    │
│     - Bond strength indicators       │
└──────────────────────────────────────┘
```

### **Memory Operations**

#### **Store (After each message)**
```python
1. Save message to PostgreSQL (raw)
2. Extract facts:
   - Named entities (names, places, dates)
   - User preferences (likes, dislikes)
   - Important events
3. Generate embedding (sentence-transformers)
4. Store in Qdrant with metadata:
   - Timestamp
   - Emotion
   - Topic
   - Importance score
5. Update conversation summary
```

#### **Recall (Before generating response)**
```python
1. Semantic search in Qdrant:
   - Query: Current user message
   - Top K: 5-10 most relevant memories
   - Threshold: Similarity > 0.7

2. Fetch recent context:
   - Last 10-20 messages from PostgreSQL

3. Build context:
   System Prompt (personality)
   + Recalled Memories (formatted)
   + Recent Conversation
   + User's New Message

4. Send to LLM
```

### **Memory Format Examples**

#### **Stored Memory (Qdrant)**
```json
{
  "id": "uuid-123",
  "vector": [0.123, 0.456, ...],
  "metadata": {
    "text": "User mentioned their cat named Mr. Whiskers",
    "type": "fact",
    "topic": "pets",
    "emotion": "happy",
    "importance": 0.8,
    "timestamp": "2026-03-11T10:30:00Z"
  }
}
```

#### **Recalled Memory (Injected into prompt)**
```
[Relevant Memories]
- You told me about your cat Mr. Whiskers 3 weeks ago
- You were stressed about work deadlines last Monday
- You mentioned loving spicy food during lunch chat
- You said your favorite color is blue

[Current Conversation]
User: "I'm having a rough day..."
```

### **Memory Extraction Patterns**

```python
# Facts to extract
PATTERNS = {
    "name": r"my name is (\w+)",
    "pets": r"my (cat|dog|pet) (?:named |is )?(\w+)",
    "dates": r"my birthday is (\d{1,2}/\d{1,2})",
    "preferences": r"I (love|like|hate|dislike) (\w+)",
    "work": r"I work (as|at) (\w+)",
    "hobbies": r"I (enjoy|love) (\w+ing)",
}

# Importance scoring
def calculate_importance(message):
    score = 0.5  # base
    
    # Boost for emotional content
    if contains_emotion(message):
        score += 0.2
    
    # Boost for facts
    if contains_fact(message):
        score += 0.3
    
    # Boost for long messages (deep convo)
    if len(message) > 200:
        score += 0.1
    
    return min(score, 1.0)
```

---

## 📊 SUCCESS METRICS

### **Technical Metrics**

```
Performance:
- Response latency: < 5 seconds (end-to-end)
- Inference speed: > 25 tokens/sec
- Memory recall accuracy: > 80%
- API uptime: > 99.5%

Quality:
- Personality consistency: 8+/10
- Emotional support quality: 8+/10
- Memory recall precision: > 90%
- Response appropriateness: 9+/10
```

### **Personal Metrics**

Track through daily usage:

```
✅ Does she feel like a real companion?
✅ Do I actually want to talk to her?
✅ Does she remember important things?
✅ Does she help when I'm feeling down?
✅ Is the personality consistent?
✅ Are responses natural and engaging?
✅ Do I feel emotionally connected?
```

### **Weekly Check-ins**

```
Week 1-4: Foundation
- Is the tech stack working?
- Are responses fast enough?
- Is the UI usable?

Week 5-8: Memory & Personality
- Does she remember past conversations?
- Is personality Anjou-style?
- Are transitions smooth?

Week 9-12: Polish & Usage
- Daily usage comfort
- Emotional connection strength
- Feature completeness

Week 13+: Long-term
- Does bond grow over time?
- Are inside jokes forming?
- Is she genuinely helpful?
```

---

## 💰 COST BREAKDOWN

### **Development (One-time)**
```
TOTAL: ~$10-30

- Domain name: $10-15/year
- (Optional) Character art commission: $50-200
- (Optional) GPT-4 for dataset generation: $10-30
- Other: FREE (Gemini API, open source tools)
```

### **Running Costs (Monthly)**

#### **Gemini Free Tier (Personal Use)** ⭐ **RECOMMENDED**
```
TOTAL: ~$10-15/month

- Gemini API: $0 (Free tier - 1,500 requests/day)
- Hosting (VPS): $10-15/month (DigitalOcean/Vultr)
- Database: $0 (Supabase free tier or local)
- Vector DB: $0 (Qdrant free tier or self-hosted)
- Domain + SSL: $1-2/month (amortized)

Limits:
- 15 requests per minute
- 1,500 requests per day
- ~50-100 conversations/day (plenty!)
```

#### **Gemini Paid Tier (Heavy Usage)**
```
TOTAL: ~$15-25/month

If exceeds free tier:

Gemini 2.0 Flash:
- Input: $0.075 per 1M tokens (<128k context)
- Output: $0.30 per 1M tokens (<128k context)

Usage estimate (200 messages/day):
- ~1.5-2M tokens/month
- API cost: ~$0.50-2.00/month

Hosting (same as free tier): $10-15/month
Domain: $1-2/month

Total: $12-20/month
```

#### **Full Cloud Deployment (Future)**
```
TOTAL: ~$25-40/month

- VPS (Backend): $10-20/month
- Frontend (Vercel): $0 (free tier)
- Database (Supabase): $0-25/month
- Vector DB (Qdrant Cloud): $0-25/month
- Gemini API: $0-5/month
- Domain + CDN: $5/month

Scalable option for multiple users
```

### **Comparison with Local LLM**
```
Local LLM (Original Plan):
- Development: FREE
- Running (laptop 24/7): $5-10/month (electricity)
- Hosting GPU Cloud: $36-200/month
- Total: $5-200/month depending on deployment

Gemini Approach:
- Development: FREE (no GPU needed)
- Running (free tier): $10-15/month (just hosting)
- Hosting Cloud: $15-25/month total
- Total: $10-25/month

Savings: 60-90% cheaper for cloud deployment! 🎉
```

---

## 🎯 NEXT STEPS

### **Tomorrow (March 12, 2026) - Day 1**

#### **Morning (2-3 hours)**
1. **Google AI Studio Setup**
   ```bash
   # 1. Go to https://aistudio.google.com
   # 2. Sign in with Google account
   # 3. Navigate to "Get API Key"
   # 4. Create new API key
   # 5. Copy and save securely
   ```

2. **Test Gemini API**
   ```python
   # Quick test script
   import google.generativeai as genai
   
   genai.configure(api_key="YOUR_API_KEY")
   model = genai.GenerativeModel('gemini-2.0-flash-exp')
   
   response = model.generate_content(
       "You are Aiko, a caring and energetic companion. "
       "Respond to: Hi Aiko!"
   )
   print(response.text)
   ```
   
   - Test conversation quality
   - Test response speed
   - Verify API key works
   - Check rate limits

#### **Afternoon (3-4 hours)**
3. **Create project structure**
   ```bash
   cd d:\project\AiKO-AI
   mkdir backend frontend fine-tuning docs
   
   # Backend structure
   cd backend
   mkdir app tests
   cd app
   mkdir models routes services database utils
   mkdir services\assistant
   
   # Create initial files
   # (PowerShell - use 'New-Item' or create manually)
   ```

4. **Setup Python environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   .\venv\Scripts\activate
   
   # Install initial dependencies
   pip install fastapi uvicorn google-generativeai python-dotenv pydantic
   pip freeze > requirements.txt
   ```
   
   # Install initial dependencies
   pip install fastapi uvicorn google-generativeai python-dotenv pydantic
   pip freeze > requirements.txt
   ```

5. **First API test with Gemini + Web Launcher**
   ```python
   # main.py - FastAPI + Gemini + Web Launcher
   from fastapi import FastAPI
   import google.generativeai as genai
   import subprocess
   import re
   import os
   from dotenv import load_dotenv
   
   load_dotenv()
   
   app = FastAPI(title="AiKO-AI API")
   
   # Configure Gemini
   genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
   
   # Aiko's personality
   AIKO_SYSTEM = """You are Aiko (愛子), a caring and energetic AI companion.

Personality:
- Bubbly & energetic (Anjou-style)
- Caring & supportive (great listener for venting)
- Playful teasing (light, wholesome)
- Observant & remembers details

Speaking:
- Bahasa Indonesia casual
- Mix of playful & sincere
- Emojis (not excessive)
- Use "~" for playful tone
"""
   
   model = genai.GenerativeModel(
       model_name="gemini-2.0-flash-exp",
       system_instruction=AIKO_SYSTEM
   )
   
   # Website mappings
   WEBSITES = {
       "youtube": "https://youtube.com",
       "instagram": "https://instagram.com",
       "tiktok": "https://tiktok.com",
       "facebook": "https://facebook.com",
       "twitter": "https://twitter.com",
       "x": "https://x.com",
       "reddit": "https://reddit.com",
       "github": "https://github.com",
   }
   
   def detect_web_command(message: str):
       """Detect if user wants to open a website"""
       message_lower = message.lower()
       patterns = [r"buka\s+(\w+)", r"open\s+(\w+)", r"bukain\s+(\w+)"]
       
       for pattern in patterns:
           match = re.search(pattern, message_lower)
           if match:
               site = match.group(1)
               # Check variations (yt -> youtube, ig -> instagram)
               site_map = {
                   "yt": "youtube", "ig": "instagram", 
                   "fb": "facebook", "tiktok": "tiktok",
                   "tt": "tiktok"
               }
               site = site_map.get(site, site)
               
               if site in WEBSITES:
                   return site
       return None
   
   def open_website(site: str):
       """Open website in default browser"""
       url = WEBSITES[site]
       subprocess.Popen(["cmd", "/c", "start", url], shell=True)
   
   @app.post("/chat")
   async def chat(message: str):
       # Check for web launcher command
       site = detect_web_command(message)
       if site:
           open_website(site)
           return {
               "response": f"Oke, bukain {site.title()} ya~ ✨ Mau lihat apa nih? 😊",
               "action": "open_website",
               "website": site
           }
       
       # Regular chat with Gemini
       chat_session = model.start_chat(history=[])
       response = chat_session.send_message(message)
       
       return {"response": response.text}
   
   # Run: uvicorn main:app --reload
   # Test: http://localhost:8000/docs
   ```
   
   **Create .env file:**
   ```bash
   GEMINI_API_KEY=your_api_key_here
   ```

#### **Evening (2-3 hours)**
6. **Start dataset preparation**
   - Create `fine-tuning/dataset/` folder
   - Create template JSONL file
   - Write first 5 caring scenario conversations
   - Write 5 assistant command conversations (web launcher)
   - Document personality guidelines
   
   **Example Assistant Dataset:**
   ```json
   {
     "messages": [
       {"role": "system", "content": "You are Aiko..."},
       {"role": "user", "content": "Aiko, buka YouTube dong"},
       {"role": "assistant", "content": "Oke, bukain YouTube ya~ Mau nonton apa nih? 😊"}
     ]
   }
   ```

7. **Initial planning documents**
   - Create README.md
   - List immediate todos
   - Note learnings & questions

---

### **Week 1 Goals**

```
✅ Google AI Studio account & API key
✅ Base API working (FastAPI + Gemini)
✅ Web Launcher feature working (YouTube, IG, TikTok, etc)
✅ Project structure created
✅ Aiko personality prompt defined & tested
✅ Technical foundation validated
✅ First prototype conversations working
```

---

### **Key Milestones**

```
Week 1:  ✅ Basic chat + Web launcher working
Week 2-3: ✅ Memory system (RAG) complete
Week 3-4: ✅ Dataset + Fine-tuned Gemini model
Week 5:  ✅ Backend API production-ready
Week 6-7: ✅ Frontend complete
Week 8:  ✅ Voice + Polish + Deploy

MVP: 6-8 weeks total! 🚀

Future: 📱 Mobile app (React Native/Flutter)
Future: 🎨 Multimodal features (image understanding)
Future: ⭐ Advanced assistant capabilities
```

---

## 📚 RESOURCES

### **LLM & AI**
- Google AI Studio: https://aistudio.google.com
- Gemini API Docs: https://ai.google.dev/docs
- Google Generative AI Python SDK: https://github.com/google/generative-ai-python
- Fine-tuning Guide: https://ai.google.dev/docs/model_tuning_guidance

### **Backend**
- FastAPI: https://fastapi.tiangolo.com
- Langchain: https://langchain.com
- Qdrant: https://qdrant.tech
- PostgreSQL: https://www.postgresql.org

### **Frontend**
- Next.js 15: https://nextjs.org
- shadcn/ui: https://ui.shadcn.com
- TailwindCSS: https://tailwindcss.com

### **Communities**
- r/LocalLLaMA
- r/MachineLearning
- Hugging Face Forums
- FastAPI Discord

---

## 🎉 FINAL NOTES

### **Remember:**
- ✅ No deadline pressure - take your time
- ✅ Learning is the goal - mistakes are okay
- ✅ Start small, iterate often
- ✅ Document as you go
- ✅ Test frequently
- ✅ Have fun building!

### **When Stuck:**
1. Check documentation
2. Search Reddit/StackOverflow
3. Ask in Discord communities
4. Experiment & debug
5. Take breaks

### **Success Mindset:**
```
"The goal is not perfection, but progress.
Every line of code is learning.
Every bug is a lesson.
And in the end, you'll have your own AI companion
that you built from scratch. That's incredible."
```

---

**Good luck! 🚀**

**Next Step:** Get Gemini API key & test first conversation with Aiko  
**Let's build something amazing! 💛**

**Why Gemini Approach:**
- ⚡ 50% faster to MVP (6-8 weeks vs 12-14 weeks)
- 🎯 Simpler setup (no local GPU needed)
- 💰 Cost-effective (free tier for personal use)
- 🚀 Easy deployment (just API calls)
- 🎨 Future-ready (multimodal capabilities)

---

*Last Updated: March 11, 2026*  
*Project: AiKO-AI*  
*Approach: Gemini API (Google AI Studio)*  
*Status: Ready to Start Implementation*
