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

### **Deployment**
- **Phase 1:** Local (personal laptop)
- **Phase 2:** Cloud (accessible dari mana saja)
- **Phase 3:** Mobile app (pocket companion)

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

## 💻 HARDWARE & MODEL

### **Hardware Specs**
```
CPU: Intel Core i5-13450HX (13th Gen)
RAM: 16 GB
GPU: NVIDIA RTX 5050 Laptop
  - VRAM: 8GB GDDR7
  - CUDA Cores: 2560
  - TDP: 100W
Storage: 476.9 GB + 119.2 GB SSD

✅ Verdict: Perfect untuk 7B-8B models
```

### **LLM Model**

**Choice:** Llama 3.1 8B Instruct (Meta)

**Why:**
- ✅ Excellent conversation quality
- ✅ 8K context window
- ✅ Strong reasoning & personality
- ✅ Open source, commercial use OK
- ✅ Proven untuk fine-tuning

**Performance Estimates:**
```
Inference: ~25-40 tokens/second
VRAM Usage: ~6-7 GB (4-bit quantization)
Response Time: 2-5 seconds
Context Window: 8K tokens (~6000 words)
```

**Installation:**
```bash
# Install Ollama from ollama.ai
ollama pull llama3.1:8b
ollama run llama3.1:8b
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
Ollama (Inference engine)
Langchain or LlamaIndex (Orchestration)
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
│Ollama│  │PostgreS│  │ Qdrant  │
│Llama │  │   QL   │  │(Vectors)│
│3.1 8B│  │        │  │         │
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
5. Send to Ollama (Llama 3.1 8B fine-tuned)
   ↓
6. Stream response to frontend (WebSocket)
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

### **PHASE 1: Quick Wins & Setup (Week 1-2)**

**Goal:** Early features + Fine-tuning prep

#### **Part A: Early Development Features (Week 1)**
- [ ] Install Ollama
- [ ] Test base Llama 3.1 8B
- [ ] **Web Launcher Feature** (Early win! 🎯)
  - [ ] Command detection ("buka YouTube", "open Instagram")
  - [ ] Website mapping (YouTube, Instagram, TikTok, Facebook, Twitter, dll)
  - [ ] Execute browser command (Windows)
  - [ ] Natural language variants ("buka YT", "tolong bukain IG")
  - [ ] Response feedback ("Oke, bukain YouTube ya~")
  - [ ] Test with real usage

#### **Part B: Fine-tuning Preparation (Week 1-2)**
- [ ] Design personality framework
- [ ] Create dataset structure (JSONL)
- [ ] Write 100 manual core conversations
  - 40-50 caring/support scenarios
  - 30-40 daily conversation
  - 20-30 playful teasing
  - 10-20 assistant commands (web launcher, reminders)
- [ ] Generate 400-900 variations dengan GPT-4
- [ ] Quality control & clean dataset
- [ ] Split dataset (train/validation: 90/10)

**Deliverables:**
- `conversations.jsonl` (500-1000 examples)
  - Companionship scenarios: 400-800 examples
  - Assistant commands: 100-200 examples
- `validation.jsonl` (50-100 examples)
- Dataset statistics report

**Web Launcher Feature:**
- ✅ Working prototype (dapat buka websites)
- ✅ Natural language detection
- ✅ Response personality consistent
- ✅ Test coverage for major sites

---

### **PHASE 2: Fine-tuning (Week 2-3)**

**Goal:** Fine-tune Llama 3.1 8B dengan personality dataset

**Tasks:**
- [ ] Setup training environment
  - [ ] Install Axolotl/Unsloth/LLaMA Factory
  - [ ] Configure CUDA & dependencies
- [ ] Configure LoRA parameters
  ```yaml
  # Example config
  base_model: llama3.1:8b
  lora_r: 16
  lora_alpha: 32
  lora_dropout: 0.05
  learning_rate: 2e-4
  batch_size: 4
  epochs: 3-4
  ```
- [ ] Start training (2-8 hours)
- [ ] Monitor loss & metrics
- [ ] Evaluate on validation set
- [ ] Test conversations manually
- [ ] Iterate if needed (adjust dataset/params)
- [ ] Merge LoRA weights
- [ ] Export final model
- [ ] Load custom model di Ollama

**Deliverables:**
- Fine-tuned model (Modelfile)
- Training logs & metrics
- Evaluation report

**Expected Results:**
- Consistent personality
- Natural Anjou-style responses
- Good emotional support quality

---

### **PHASE 3: Backend Core (Week 3-5)**

**Goal:** Build API server dengan LLM integration

**Week 3:**
- [ ] Initialize FastAPI project
- [ ] Setup project structure
- [ ] Configure environment (.env)
- [ ] Integrate Ollama
  - [ ] Test connection
  - [ ] Chat completion endpoint
  - [ ] Streaming responses
- [ ] Basic authentication
  - [ ] User registration
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

### **Training Configuration**

**LoRA Parameters:**
```yaml
base_model: llama3.1:8b
adapter: lora

# LoRA config
lora_r: 16              # Rank (higher = more params)
lora_alpha: 32          # Scaling factor
lora_dropout: 0.05      # Regularization
target_modules:         # Which layers to adapt
  - q_proj
  - k_proj
  - v_proj
  - o_proj

# Training hyperparameters
learning_rate: 2e-4
batch_size: 4           # Adjust based on VRAM
gradient_accumulation: 4
epochs: 3-4
warmup_steps: 100
max_seq_length: 2048

# Optimization
optimizer: adamw
scheduler: cosine
weight_decay: 0.01
```

**Expected Training Time:**
- Dataset: 1000 examples
- Epochs: 3-4
- Batch size: 4
- RTX 5050 (8GB VRAM)
- **Duration: 4-8 hours**

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
TOTAL: ~$15-30

- Domain name: $10-15/year
- (Optional) Character art commission: $50-200
- Other: FREE (all open source)
```

### **Running Costs (Monthly)**

#### **Full Local (Personal Use)**
```
TOTAL: ~$5-10/month

- Electricity (laptop running): $5-10/month
- No API costs: $0
- No hosting: $0
- Database: Local (free)
```

#### **Hybrid (Local + Cloud Access) - Future**
```
TOTAL: ~$25-60/month

Option A: RunPod (GPU Cloud)
- GPU instance: $0.30-0.50/hour
- Average usage: 4 hrs/day = ~$40/month
- Storage: $5/month
- Domain + CDN: $5/month

Option B: VPS (No dedicated GPU, use local for inference)
- VPS (Frontend + DB): $10-20/month
- Domain + CDN: $5/month
- Inference: Local laptop (remote access)

Option C: Serverless (Modal/Replicate)
- Pay per use: $0.01-0.10/user/day
- Personal use: ~$5-15/month
```

### **Data Costs**
```
FREE for LLM (no OpenAI/Anthropic API)

Optional (if using for dataset generation):
- GPT-4 for dataset generation: $10-30 (one-time)
- Total: ~1M tokens = $20-40
```

---

## 🎯 NEXT STEPS

### **Tomorrow (March 12, 2026) - Day 1**

#### **Morning (2-3 hours)**
1. **Install Ollama**
   ```bash
   # Download from ollama.ai
   # Install untuk Windows
   
   # Pull base model
   ollama pull llama3.1:8b
   
   # Test run
   ollama run llama3.1:8b
   # Try: "Hi, can you act as a caring and energetic companion?"
   ```

2. **Test base model capabilities**
   - Test conversation quality
   - Test personality following (dengan system prompts)
   - Measure inference speed
   - Check VRAM usage

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
   
   # Create initial files
   touch main.py config.py __init__.py
   touch requirements.txt .env.example
   ```

4. **Setup Python environment**
   ```bash
   # Create virtual environment
   python -m venv venv
   venv\Scripts\activate
   
   # Install initial dependencies
   pip install fastapi uvicorn ollama python-dotenv pydantic
   pip freeze > requirements.txt
   ```

5. **First API test with Web Launcher**
   ```python
   # main.py - Basic FastAPI + Ollama + Web Launcher
   from fastapi import FastAPI
   import ollama
   import subprocess
   import re
   
   app = FastAPI(title="AiKO-AI API")
   
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
   def chat(message: str):
       # Check for web launcher command
       site = detect_web_command(message)
       if site:
           open_website(site)
           return {
               "response": f"Oke, bukain {site.title()} ya~ ✨",
               "action": "open_website",
               "website": site
           }
       
       # Regular chat
       response = ollama.chat(
           model="llama3.1:8b",
           messages=[{"role": "user", "content": message}]
       )
       return {"response": response['message']['content']}
   
   # Run: uvicorn main:app --reload
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
✅ Ollama installed & tested
✅ Base API working (FastAPI + Ollama)
✅ Web Launcher feature working (YouTube, IG, TikTok, etc)
✅ Project structure created
✅ 50 core conversations written (including assistant commands)
✅ Personality framework defined
✅ Technical foundation validated
```

---

### **Key Milestones**

```
Week 2:  ✅ Dataset complete (500-1000 examples)
Week 3:  ✅ Fine-tuned model ready
Week 5:  ✅ Backend API complete
Week 7:  ✅ Memory system working
Week 10: ✅ Frontend complete
Week 12: ✅ Voice integration
Week 14: ✅ Personal deployment & daily use

Future: ☁️ Cloud deployment
Future: 📱 Mobile app
Future: ⭐ Advanced features
```

---

## 📚 RESOURCES

### **LLM & Fine-tuning**
- Ollama: https://ollama.ai
- Axolotl: https://github.com/OpenAccess-AI-Collective/axolotl
- Unsloth: https://github.com/unslothai/unsloth
- LLaMA Factory: https://github.com/hiyouga/LLaMA-Factory

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

**Next Step:** Install Ollama & test Llama 3.1 8B
**Let's build something amazing! 💛**

---

*Last Updated: March 11, 2026*
*Project: AiKO-AI*
*Status: Ready to Start Implementation*
