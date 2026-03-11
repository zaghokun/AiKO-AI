# 🚀 Quick Start: Fine-tuning Aiko

Fast track guide untuk fine-tune Aiko personality!

---

## ⚡ 5-Minute Setup

### 1. Validate Dataset (30 seconds)
```bash
cd backend/fine-tuning/scripts
python validate_dataset.py
```

Expected: ✅ All valid! (50 examples total)

### 2. Combine Datasets (30 seconds)
```bash
python generate_dataset.py
```

Output: `combined_dataset.jsonl` created

### 3. Upload to Google AI Studio (3 minutes)

📍 **Go to:** https://aistudio.google.com

1. Click **"Tuned models"** (left sidebar)
2. Click **"New tuned model"**
3. Select base model: `gemini-2.0-flash-exp`
4. Upload: `backend/fine-tuning/datasets/combined_dataset.jsonl`
5. Set name: `aiko-personality-v1`
6. Epochs: **3**
7. Click **"Start tuning"**

⏳ **Wait: 30 minutes - 2 hours**

---

## ✅ After Training Complete

### 1. Get Model ID

In Google AI Studio, copy your model name:
```
tunedModels/aiko-personality-v1-1234567890
```

### 2. Test in AI Studio

Try these prompts:
- "Halo Aiko!"
- "Aku lagi sedih nih"
- "Kamu cantik ga sih?"
- "Buka YouTube dong"

Compare with base model. Better personality? ✨

### 3. Update Backend

Edit `backend/app/services/gemini_service.py`:

```python
# Line ~53 - Change model_name
self.model = genai.GenerativeModel(
    model_name="tunedModels/aiko-personality-v1-1234567890",  # ← Paste your model ID
    system_instruction=self.AIKO_SYSTEM_INSTRUCTION,
)
```

### 4. Restart Server

```powershell
cd backend
python -m app.main
```

### 5. Test in Web Chat

Open: http://localhost:8000/test-chat

Try conversations and compare!

---

## 📊 Evaluation

Check if fine-tuned Aiko is better at:
- [ ] Consistent personality (caring + playful)
- [ ] Natural emoji usage
- [ ] Indonesian-English mixing
- [ ] Anjou-style teasing
- [ ] Emotional support
- [ ] Assistant commands

---

## 🔄 Next Iteration

**To improve further:**

1. Add more examples (target: 200-500)
2. Balance categories
3. Fine-tune again (version v2)
4. Compare v1 vs v2

---

## 📚 Full Documentation

- [README.md](README.md) - Complete guide
- [Dataset Examples](examples/dataset_examples.md) - Format reference
- [Gemini Docs](https://ai.google.dev/gemini-api/docs/model-tuning) - Official docs

---

**Questions?** Check [README.md](README.md) troubleshooting section!

**Ready? GO! 🚀💕**
