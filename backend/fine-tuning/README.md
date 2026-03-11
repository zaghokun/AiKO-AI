# 🎯 Fine-tuning Guide for Aiko

Complete guide untuk fine-tune Gemini model dengan personality Aiko.

---

## 📚 Dataset Overview

**Total Examples: 50** (Test dataset untuk initial fine-tuning)

### Categories:

1. **01_caring_support.jsonl** - 15 examples (30%)
   - Emotional support conversations
   - Venting and problem-solving
   - Encouraging and validating feelings

2. **02_daily_conversation.jsonl** - 15 examples (30%)
   - Greetings and check-ins
   - Casual daily chat
   - Small talk and mood sharing

3. **03_playful_teasing.jsonl** - 10 examples (20%)
   - Anjou-style playful teasing
   - Light flirting and banter
   - Wholesome jokes

4. **04_assistant_commands.jsonl** - 5 examples (10%)
   - Web launcher commands
   - Task requests
   - Assistant functionality

5. **05_mood_transitions.jsonl** - 5 examples (10%)
   - Mood changes and shifts
   - Adapting tone to user's state

**Target untuk production: 500-1000 examples**

---

## 🔧 Setup & Validation

### 1. Validate Dataset

```bash
cd backend/fine-tuning/scripts
python validate_dataset.py
```

Expected output:
```
✅ 01_caring_support.jsonl: 15 examples
✅ 02_daily_conversation.jsonl: 15 examples
✅ 03_playful_teasing.jsonl: 10 examples
✅ 04_assistant_commands.jsonl: 5 examples
✅ 05_mood_transitions.jsonl: 5 examples
==================================================
Total examples: 50
Status: ✅ All valid!
==================================================
```

### 2. Combine Datasets

```bash
python generate_dataset.py
```

This creates `combined_dataset.jsonl` with all examples shuffled.

---

## 🚀 Upload to Google AI Studio

### Step 1: Prepare File

1. Navigate to `backend/fine-tuning/datasets/`
2. Locate `combined_dataset.jsonl`
3. Verify file size (should be ~15-20KB for 50 examples)

### Step 2: Access Google AI Studio

1. Open https://aistudio.google.com
2. Sign in with your Google account
3. Click **"Tuned models"** in left sidebar
4. Click **"New tuned model"** button

### Step 3: Configure Fine-tuning

**Model Selection:**
- Base model: `gemini-1.5-flash-002` or `gemini-2.0-flash-exp`
- (Use Flash for faster training & cheaper)

**Upload Dataset:**
1. Click "Upload file" or drag-and-drop
2. Select `combined_dataset.jsonl`
3. Wait for validation (should show 50 examples)

**Training Configuration:**
- **Epochs**: 3-5 (start with 3)
  - More epochs = better learning, but risk overfitting
- **Learning rate**: Auto (default)
- **Batch size**: Auto (default)

**Model Name:**
- Suggested: `aiko-personality-v1`
- Use versioning for future iterations

### Step 4: Start Training

1. Review configuration
2. Click **"Start tuning"**
3. Training will take: **30 minutes - 2 hours**
   - Free tier: Can be slower
   - Paid tier: Faster

### Step 5: Monitor Progress

You'll see:
- Training status (Queued → Running → Completed)
- Loss metrics (should decrease)
- Estimated time remaining

---

## ✅ Post-Training

### 1. Test Fine-tuned Model

Once complete, you'll get a model ID:
```
tunedModels/aiko-personality-v1-abc123xyz
```

Test in AI Studio:
1. Click on your tuned model
2. Try test prompts:
   - "Halo Aiko!"
   - "Aku lagi sedih nih"
   - "Buka YouTube dong"
3. Compare with base model

### 2. Update Backend Code

Edit `backend/app/services/gemini_service.py`:

```python
# Change this line:
model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",  # ← Base model
    system_instruction=self.AIKO_SYSTEM_INSTRUCTION,
)

# To this:
model = genai.GenerativeModel(
    model_name="tunedModels/aiko-personality-v1-abc123xyz",  # ← Your tuned model
    # Note: Fine-tuned models already have personality built-in
    # But you can still use system_instruction for context
)
```

### 3. Test in Your App

1. Restart server
2. Chat with Aiko via web interface
3. Compare responses:
   - More consistent personality?
   - Better Anjou-style teasing?
   - More natural Indonesian mix?

---

## 📊 Evaluation Checklist

Compare **Base Model** vs **Fine-tuned Model**:

- [ ] Personality consistency (energetic, caring, playful)
- [ ] Natural emoji usage (not too much, not too little)
- [ ] Indonesian-English code-mixing (natural flow)
- [ ] Anjou-style teasing (playful but caring)
- [ ] Emotional support quality
- [ ] Assistant command handling
- [ ] Response length (not too short, not too long)

---

## 🔄 Iteration Plan

### Phase 1: Test (Current - 50 examples)
- **Goal**: Validate fine-tuning works
- **Dataset**: 50 examples
- **Test**: Basic personality consistency

### Phase 2: Expand (200 examples)
- Multiply each category by 4x
- Add more conversation variations
- Test improvement

### Phase 3: Production (500-1000 examples)
- Full dataset with diverse scenarios
- Include edge cases
- Polish personality traits
- Final production model

---

## 💡 Tips for Better Fine-tuning

### 1. Dataset Quality > Quantity
- 50 high-quality examples > 200 mediocre ones
- Maintain consistent personality across all examples
- Proofread for typos and formatting

### 2. Balance Categories
- Don't overfit on one category
- Maintain distribution (40% caring, 30% daily, etc.)

### 3. Natural Conversations
- Write how people actually talk
- Include typos if realistic (but don't overdo)
- Mix Indonesian and English naturally

### 4. Emoji Usage
- 1-3 emojis per response (Aiko's style)
- Place naturally, not forced
- Match emotion of message

### 5. Length Consistency
- Not too short (min 1 sentence)
- Not too long (max 3-4 sentences usually)
- Match conversation context

---

## 🎓 Examples to Add Later

### More Caring/Support:
- Breakup comfort
- Job loss support
- Health anxiety
- Family conflict
- Academic stress

### More Daily:
- Weather chat
- Hobby discussions
- TV show/movie talk
- Food conversations
- Weekend plans

### More Playful:
- Compliment fishing
- Jealousy play
- Cute demands
- Playful arguments
- Victory celebrations

### More Assistant:
- Calendar management
- Search queries
- Reminder setting
- Information lookup
- Task breakdown

---

## 📈 Cost (Google AI Studio)

**Free Tier:**
- Fine-tuning: FREE for Flash models
- Storage: First model FREE
- Inference: 1,500 requests/day FREE

**Paid Tier (if exceeded):**
- Fine-tuning: ~$0.001 per 1000 examples
- 50 examples = essentially FREE
- 1000 examples = ~$1

**Very affordable!** 💰

---

## 🆘 Troubleshooting

**Q: Validation failed - malformed JSON**
- Check each line is valid JSON
- Use `validate_dataset.py` to find errors
- Common issue: Extra commas or quotes

**Q: Training taking too long**
- Free tier can be slow (wait it out)
- Upgrade to paid tier for faster
- 50 examples should be quick though

**Q: Model not improving**
- Try more epochs (5 instead of 3)
- Check dataset quality
- Need more examples (add to 100+)

**Q: Model too different from original**
- Reduce epochs (3 → 2)
- Check for overfitting
- Balance dataset categories

**Q: Can't find model ID**
- Go to "Tuned models" page
- Click on your model
- Copy full model name including `tunedModels/`

---

## 🎯 Success Metrics

After fine-tuning, Aiko should:
- ✅ Respond consistently with caring + playful personality
- ✅ Mix Indonesian and English naturally
- ✅ Use emojis appropriately (not too much)
- ✅ Show empathy in support scenarios
- ✅ Tease playfully without being mean
- ✅ Handle assistant commands naturally
- ✅ Adapt tone to user's mood

---

## 📞 Next Steps

1. ✅ Validate datasets (`python validate_dataset.py`)
2. ✅ Combine datasets (`python generate_dataset.py`)
3. 🚀 Upload to Google AI Studio
4. ⏳ Wait for training (30min-2h)
5. 🧪 Test fine-tuned model
6. 🔧 Update backend code
7. 💬 Chat with improved Aiko!
8. 📝 Gather feedback
9. 🔄 Iterate with more examples

---

**Good luck with fine-tuning! 🚀💕**

Questions? Issues? Check troubleshooting section or review Gemini docs:
https://ai.google.dev/gemini-api/docs/model-tuning
