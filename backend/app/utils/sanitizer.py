"""
Input sanitization utilities
Prevent XSS, SQL injection, and other attacks
"""

import re
import html
from typing import Optional


class InputSanitizer:
    """Sanitize user input to prevent security vulnerabilities"""
    
    # Dangerous patterns to detect
    SQL_INJECTION_PATTERNS = [
        r"(\bUNION\b.*\bSELECT\b)",
        r"(\bDROP\b.*\bTABLE\b)",
        r"(\bINSERT\b.*\bINTO\b)",
        r"(\bDELETE\b.*\bFROM\b)",
        r"(\bUPDATE\b.*\bSET\b)",
        r"(--|\#|\/\*|\*\/)",  # SQL comments
        r"(\bOR\b.*=.*)",
        r"(\bAND\b.*=.*)",
    ]
    
    XSS_PATTERNS = [
        r"<script[^>]*>.*?</script>",
        r"javascript:",
        r"on\w+\s*=",  # Event handlers like onclick, onerror
        r"<iframe",
        r"<object",
        r"<embed",
    ]
    
    @staticmethod
    def sanitize_html(text: str) -> str:
        """
        Escape HTML special characters
        
        Args:
            text: Input text
            
        Returns:
            HTML-escaped text
        """
        return html.escape(text)
    
    @staticmethod
    def remove_html_tags(text: str) -> str:
        """
        Remove all HTML tags from text
        
        Args:
            text: Input text with potential HTML
            
        Returns:
            Clean text without HTML tags
        """
        clean = re.compile('<.*?>')
        return re.sub(clean, '', text)
    
    @staticmethod
    def sanitize_input(text: str, max_length: int = 10000) -> str:
        """
        Comprehensive input sanitization
        
        Args:
            text: User input text
            max_length: Maximum allowed length
            
        Returns:
            Sanitized text
        """
        if not text:
            return ""
        
        # Trim to max length
        text = text[:max_length]
        
        # Remove null bytes
        text = text.replace('\x00', '')
        
        # Normalize whitespace
        text = ' '.join(text.split())
        
        return text
    
    @staticmethod
    def detect_sql_injection(text: str) -> bool:
        """
        Detect potential SQL injection attempts
        
        Args:
            text: Input text to check
            
        Returns:
            True if suspicious pattern detected
        """
        text_upper = text.upper()
        
        for pattern in InputSanitizer.SQL_INJECTION_PATTERNS:
            if re.search(pattern, text_upper, re.IGNORECASE):
                return True
        
        return False
    
    @staticmethod
    def detect_xss(text: str) -> bool:
        """
        Detect potential XSS attempts
        
        Args:
            text: Input text to check
            
        Returns:
            True if suspicious pattern detected
        """
        for pattern in InputSanitizer.XSS_PATTERNS:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        
        return False
    
    @staticmethod
    def sanitize_chat_message(message: str) -> str:
        """
        Sanitize chat message input
        
        Args:
            message: Chat message from user
            
        Returns:
            Sanitized message
        """
        # Basic sanitization
        message = InputSanitizer.sanitize_input(message, max_length=5000)
        
        # Remove HTML tags but keep the text
        message = InputSanitizer.remove_html_tags(message)
        
        # Trim whitespace
        message = message.strip()
        
        return message
    
    @staticmethod
    def validate_username(username: str) -> tuple[bool, Optional[str]]:
        """
        Validate username format
        
        Args:
            username: Username to validate
            
        Returns:
            (is_valid, error_message)
        """
        if not username:
            return False, "Username is required"
        
        if len(username) < 3:
            return False, "Username must be at least 3 characters"
        
        if len(username) > 50:
            return False, "Username must be at most 50 characters"
        
        # Only alphanumeric and underscore
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return False, "Username can only contain letters, numbers, and underscores"
        
        return True, None
    
    @staticmethod
    def validate_email(email: str) -> tuple[bool, Optional[str]]:
        """
        Validate email format
        
        Args:
            email: Email to validate
            
        Returns:
            (is_valid, error_message)
        """
        if not email:
            return False, "Email is required"
        
        # Simple email regex
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        if not re.match(email_pattern, email):
            return False, "Invalid email format"
        
        if len(email) > 255:
            return False, "Email is too long"
        
        return True, None


# Global sanitizer instance
sanitizer = InputSanitizer()
