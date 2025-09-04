"""
Validation modules for email, password, and other data validation.
"""

import re
from typing import List, Optional


class EmailValidator:
    """Email validation utility class."""
    
    # Basic email regex pattern
    EMAIL_PATTERN = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    
    @classmethod
    def is_valid(cls, email: str) -> bool:
        """Validate email format using regex."""
        if not isinstance(email, str):
            return False
        
        email = email.strip()
        if not email:
            return False
        
        return bool(re.match(cls.EMAIL_PATTERN, email))
    
    @classmethod
    def validate(cls, email: str) -> str:
        """Validate and return cleaned email, raise ValueError if invalid."""
        if not isinstance(email, str):
            raise TypeError("Email must be a string")
        
        email = email.strip().lower()
        
        if not email:
            raise ValueError("Email cannot be empty")
        
        if not cls.is_valid(email):
            raise ValueError("Invalid email format")
        
        return email
    
    @classmethod
    def get_domain(cls, email: str) -> Optional[str]:
        """Extract domain from a valid email address."""
        if not cls.is_valid(email):
            return None
        
        return email.split('@')[1].lower()
    
    @classmethod
    def get_username(cls, email: str) -> Optional[str]:
        """Extract username part from a valid email address."""
        if not cls.is_valid(email):
            return None
        
        return email.split('@')[0].lower()


class PasswordValidator:
    """Password validation utility class."""
    
    def __init__(self, min_length: int = 8, max_length: int = 128,
                 require_uppercase: bool = True, require_lowercase: bool = True,
                 require_digits: bool = True, require_special: bool = True,
                 special_chars: str = "!@#$%^&*()_+-=[]{}|;:,.<>?"):
        """
        Initialize password validator with configurable requirements.
        
        Args:
            min_length: Minimum password length
            max_length: Maximum password length
            require_uppercase: Require at least one uppercase letter
            require_lowercase: Require at least one lowercase letter
            require_digits: Require at least one digit
            require_special: Require at least one special character
            special_chars: String of allowed special characters
        """
        self.min_length = min_length
        self.max_length = max_length
        self.require_uppercase = require_uppercase
        self.require_lowercase = require_lowercase
        self.require_digits = require_digits
        self.require_special = require_special
        self.special_chars = special_chars
    
    def validate(self, password: str) -> List[str]:
        """
        Validate password and return list of error messages.
        Empty list means password is valid.
        """
        if not isinstance(password, str):
            return ["Password must be a string"]
        
        errors = []
        
        # Check length
        if len(password) < self.min_length:
            errors.append(f"Password must be at least {self.min_length} characters long")
        
        if len(password) > self.max_length:
            errors.append(f"Password must be no more than {self.max_length} characters long")
        
        # Check character requirements
        if self.require_uppercase and not any(c.isupper() for c in password):
            errors.append("Password must contain at least one uppercase letter")
        
        if self.require_lowercase and not any(c.islower() for c in password):
            errors.append("Password must contain at least one lowercase letter")
        
        if self.require_digits and not any(c.isdigit() for c in password):
            errors.append("Password must contain at least one digit")
        
        if self.require_special and not any(c in self.special_chars for c in password):
            errors.append("Password must contain at least one special character")
        
        return errors
    
    def is_valid(self, password: str) -> bool:
        """Check if password meets all requirements."""
        return len(self.validate(password)) == 0
    
    def get_strength_score(self, password: str) -> int:
        """
        Calculate password strength score (0-100).
        Higher score indicates stronger password.
        """
        if not isinstance(password, str):
            return 0
        
        score = 0
        
        # Length scoring (up to 30 points)
        if len(password) >= self.min_length:
            length_score = min(30, (len(password) - self.min_length + 1) * 3)
            score += length_score
        
        # Character diversity scoring (up to 70 points)
        if any(c.isupper() for c in password):
            score += 15
        
        if any(c.islower() for c in password):
            score += 15
        
        if any(c.isdigit() for c in password):
            score += 15
        
        if any(c in self.special_chars for c in password):
            score += 15
        
        # Bonus for very long passwords
        if len(password) > 12:
            score += 5
        
        if len(password) > 16:
            score += 5
        
        return min(100, score)
    
    def get_strength_level(self, password: str) -> str:
        """Get password strength level as a string."""
        score = self.get_strength_score(password)
        
        if score < 30:
            return "Very Weak"
        elif score < 50:
            return "Weak"
        elif score < 70:
            return "Medium"
        elif score < 90:
            return "Strong"
        else:
            return "Very Strong"


class DataValidator:
    """General data validation utility class."""
    
    @staticmethod
    def is_positive_integer(value) -> bool:
        """Check if value is a positive integer."""
        return isinstance(value, int) and value > 0
    
    @staticmethod
    def is_non_negative_integer(value) -> bool:
        """Check if value is a non-negative integer."""
        return isinstance(value, int) and value >= 0
    
    @staticmethod
    def is_valid_phone(phone: str, country_code: str = "US") -> bool:
        """Validate phone number format (basic US format)."""
        if not isinstance(phone, str):
            return False
        
        # Remove common formatting
        clean_phone = re.sub(r'[^\d]', '', phone)
        
        if country_code == "US":
            # US phone numbers should be 10 digits
            return len(clean_phone) == 10
        
        # Basic international format (7-15 digits)
        return 7 <= len(clean_phone) <= 15
    
    @staticmethod
    def is_valid_url(url: str) -> bool:
        """Basic URL validation."""
        if not isinstance(url, str):
            return False
        
        url_pattern = r'^https?://.+\..+'
        return bool(re.match(url_pattern, url))
    
    @staticmethod
    def sanitize_string(text: str, max_length: int = 1000) -> str:
        """Sanitize string by removing dangerous characters and limiting length."""
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        
        # Remove potentially dangerous characters
        sanitized = re.sub(r'[<>\"\'&]', '', text)
        
        # Limit length
        if len(sanitized) > max_length:
            sanitized = sanitized[:max_length]
        
        return sanitized.strip()
