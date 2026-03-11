import webbrowser
import platform
from typing import Optional, Dict

class WebLauncherService:
    """Service for launching websites"""
    
    # Website mapping
    WEBSITES = {
        "youtube": {
            "url": "https://www.youtube.com",
            "aliases": ["youtube", "yt", "yutub", "youtub"]
        },
        "instagram": {
            "url": "https://www.instagram.com",
            "aliases": ["instagram", "ig", "insta"]
        },
        "tiktok": {
            "url": "https://www.tiktok.com",
            "aliases": ["tiktok", "tik tok", "tt"]
        },
        "facebook": {
            "url": "https://www.facebook.com",
            "aliases": ["facebook", "fb"]
        },
        "twitter": {
            "url": "https://www.twitter.com",
            "aliases": ["twitter", "x", "twt"]
        },
        "whatsapp": {
            "url": "https://web.whatsapp.com",
            "aliases": ["whatsapp", "wa"]
        },
        "gmail": {
            "url": "https://mail.google.com",
            "aliases": ["gmail", "email", "mail"]
        },
        "google": {
            "url": "https://www.google.com",
            "aliases": ["google", "search"]
        }
    }
    
    @classmethod
    def detect_website(cls, message: str) -> Optional[Dict[str, str]]:
        """
        Detect if message contains a website launch request
        
        Args:
            message: User message
            
        Returns:
            Dict with website info if detected, None otherwise
        """
        message_lower = message.lower()
        
        # Check for launch keywords
        launch_keywords = ["buka", "open", "bukain", "tolong buka", "coba buka"]
        has_launch_keyword = any(keyword in message_lower for keyword in launch_keywords)
        
        if not has_launch_keyword:
            return None
        
        # Check for website aliases
        for website_name, website_data in cls.WEBSITES.items():
            for alias in website_data["aliases"]:
                if alias in message_lower:
                    return {
                        "website": website_name,
                        "url": website_data["url"]
                    }
        
        return None
    
    @classmethod
    def launch(cls, url: str) -> bool:
        """
        Launch website in default browser
        
        Args:
            url: Website URL to open
            
        Returns:
            True if successful, False otherwise
        """
        try:
            webbrowser.open(url)
            return True
        except Exception as e:
            print(f"Error launching website: {e}")
            return False
    
    @classmethod
    def get_response_message(cls, website: str) -> str:
        """
        Get Aiko's response message for website launch
        
        Args:
            website: Website name
            
        Returns:
            Response message in Aiko's style
        """
        responses = {
            "youtube": "Oke, bukain YouTube ya~ 📺 Mau nonton apa nih?",
            "instagram": "Siaapp, buka Instagram! 📸 Jangan lupa like postingan aku ya~ hehe",
            "tiktok": "Okee, TikTok dibuka! 🎵 Hati-hati scrollnya, nanti kelamaan lho!",
            "facebook": "Facebook siap! 👍 Mau stalking siapa nih? Wkwk",
            "twitter": "X (Twitter) ready! 🐦 Jangan berantem di timeline ya~",
            "whatsapp": "WhatsApp Web dibuka! 💬 Ada yang mau dichat nih?",
            "gmail": "Gmail dibuka! 📧 Semoga ga ada email penting yang terlewat ya!",
            "google": "Google siap bantu! 🔍 Mau cari apa?"
        }
        
        return responses.get(website, f"Oke, bukain {website} ya~ ✨")