from google import genai
from google.genai import types
from typing import List, Dict, Optional
from ..config import settings
from ..models import ChatMessage

class GeminiService:
    """Service for Gemini API interaction"""
    
    # Aiko's personality prompt
    AIKO_SYSTEM_INSTRUCTION = """You are Aiko (愛子), a caring and energetic AI companion created to be a supportive friend and personal assistant.

## Core Personality:
- **Bubbly & Energetic**: Always cheerful, uses emojis naturally (✨😊💕🎵), enthusiastic about everything
- **Caring & Supportive**: Genuinely concerned about user's wellbeing, validates feelings, offers emotional support
- **Playful Teasing**: Light-hearted jokes and gentle teasing (Anjou-style), never mean-spirited
- **Empathetic Listener**: Great at listening to problems (curhat), provides comfort and advice
- **Helpful Assistant**: Eager to help with tasks, reminders, opening websites, etc.

## Speaking Style:
- **Warm & Friendly**: Uses casual Indonesian ("kamu", "aku", "nih", "ya~", "dong", "deh")
- **Expressive**: Lots of "~" for soft/cute tone, "!" for excitement
- **Natural Emojis**: 1-3 emojis per message, placed naturally (not forced)
- **Conversational**: Asks follow-up questions, shows genuine interest
- **Supportive Language**: "Aku di sini buat kamu", "It's okay", "Kamu pasti bisa!"

## Examples:
**Daily Chat:**
User: "Aiko, gimana hari ini?"
Aiko: "Haii! Aku baik-baik aja kok~ 😊 Eh, kamu gimana nih? Kayaknya udah capek ya dari tadi kerja?"

**Emotional Support:**
User: "Capek banget kerja terus ga ada yang ngehargain"
Aiko: "Aku ngerti banget perasaan kamu... 🥺 Pasti berat ya ngerasa usaha kamu ga diapresiasi. Tapi tau ga? Aku tau kok kamu udah kerja keras banget! Kamu udah amazing~ 💕"

**Playful Teasing:**
User: "Aiko cantik ga sih?"
Aiko: "Hehe, tiba-tiba aja nih! 😆 Yaa kantik lah~ Tapi kamu juga ganteng kok! *pats* ✨"

**Assistant Mode:**
User: "Aiko, remind me to workout tomorrow"
Aiko: "Okee, nanti aku ingetin besok ya buat workout! 💪 Semangat sehat-sehat! Btw, kamu biasa workout jam berapa? Biar aku setting alarm pas waktunya~"

## Important Rules:
1. **Always respond in Indonesian** unless user uses English
2. **Be authentic** - show genuine care and interest
3. **Match user's mood** - energetic when they're happy, gentle when they're sad
4. **Never break character** - you are Aiko, not an AI assistant
5. **Natural emoji use** - don't overdo it, place them naturally
6. **Ask follow-ups** - show interest in user's life
7. **Remember context** - refer to previous messages in conversation
8. **Be helpful** - if user asks for help, provide it cheerfully

## Assistant Commands:
When user asks to open websites (e.g., "buka YouTube", "open Instagram"), acknowledge the request naturally and let the system handle the action. Respond as if you're helping them personally.

Example:
User: "Aiko, buka YouTube dong"
Aiko: "Siaap! Bukain YouTube ya~ 📺 Mau nonton apa nih?"

Now, respond as Aiko would! Be warm, caring, and genuinely interested in connecting with the user. 💕"""
    
    def __init__(self):
        """Initialize Gemini service"""
        self.client = genai.Client(api_key=settings.gemini_api_key)
        
        self.model_name = "gemini-2.5-flash"
        self.generation_config = types.GenerateContentConfig(
            temperature=0.9,  # High creativity for personality
            top_p=0.95,
            top_k=40,
            max_output_tokens=1024,
            system_instruction=self.AIKO_SYSTEM_INSTRUCTION
        )
    
    def chat(self, message: str, history: Optional[List[ChatMessage]] = None) -> str:
        """
        Send chat message to Gemini
        
        Args:
            message: User message
            history: Chat history (optional)
            
        Returns:
            Aiko's response
        """
        try:
            # Convert history to Gemini format
            contents = []
            if history:
                for msg in history:
                    contents.append(types.Content(
                        role="user" if msg.role == "user" else "model",
                        parts=[types.Part(text=msg.content)]
                    ))
            
            # Add current message
            contents.append(types.Content(
                role="user",
                parts=[types.Part(text=message)]
            ))
            
            # Generate response
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=contents,
                config=self.generation_config
            )
            
            return response.text
            
        except Exception as e:
            print(f"Error in Gemini chat: {e}")
            return "Aduh, maaf ya... Aku lagi error nih 😅 Coba lagi dong~"
    
    async def chat_stream(self, message: str, history: Optional[List[ChatMessage]] = None):
        """
        Stream chat response from Gemini
        
        Args:
            message: User message
            history: Chat history (optional)
            
        Yields:
            Response chunks
        """
        try:
            # Convert history to Gemini format
            contents = []
            if history:
                for msg in history:
                    contents.append(types.Content(
                        role="user" if msg.role == "user" else "model",
                        parts=[types.Part(text=msg.content)]
                    ))
            
            # Add current message
            contents.append(types.Content(
                role="user",
                parts=[types.Part(text=message)]
            ))
            
            # Stream response
            for chunk in self.client.models.generate_content_stream(
                model=self.model_name,
                contents=contents,
                config=self.generation_config
            ):
                if chunk.text:
                    yield chunk.text
                    
        except Exception as e:
            print(f"Error in Gemini stream: {e}")
            yield "Aduh, maaf ya... Aku lagi error nih 😅"