"""
User management module providing User and UserManager classes.
"""

from datetime import datetime
from typing import List, Optional, Dict, Any
import uuid
import hashlib


class User:
    """Represents a user with basic information and authentication."""
    
    def __init__(self, username: str, email: str, password: str, full_name: str = ""):
        if not username or not username.strip():
            raise ValueError("Username cannot be empty")
        if not email or not email.strip():
            raise ValueError("Email cannot be empty")
        if not password or len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")
        
        self.id = str(uuid.uuid4())
        self.username = username.strip().lower()
        self.email = email.strip().lower()
        self.full_name = full_name.strip()
        self._password_hash = self._hash_password(password)
        self.created_at = datetime.now()
        self.last_login: Optional[datetime] = None
        self.is_active = True
        self.is_admin = False
    
    def _hash_password(self, password: str) -> str:
        """Hash a password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def check_password(self, password: str) -> bool:
        """Verify a password against the stored hash."""
        return self._password_hash == self._hash_password(password)
    
    def change_password(self, old_password: str, new_password: str) -> bool:
        """Change the user's password if the old password is correct."""
        if not self.check_password(old_password):
            return False
        
        if len(new_password) < 6:
            raise ValueError("New password must be at least 6 characters long")
        
        self._password_hash = self._hash_password(new_password)
        return True
    
    def update_email(self, new_email: str) -> None:
        """Update the user's email address."""
        if not new_email or not new_email.strip():
            raise ValueError("Email cannot be empty")
        
        self.email = new_email.strip().lower()
    
    def update_full_name(self, full_name: str) -> None:
        """Update the user's full name."""
        self.full_name = full_name.strip()
    
    def login(self) -> None:
        """Record a login timestamp."""
        self.last_login = datetime.now()
    
    def deactivate(self) -> None:
        """Deactivate the user account."""
        self.is_active = False
    
    def activate(self) -> None:
        """Activate the user account."""
        self.is_active = True
    
    def make_admin(self) -> None:
        """Grant admin privileges to the user."""
        self.is_admin = True
    
    def remove_admin(self) -> None:
        """Remove admin privileges from the user."""
        self.is_admin = False
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert user to dictionary representation (excluding password hash)."""
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name,
            "created_at": self.created_at.isoformat(),
            "last_login": self.last_login.isoformat() if self.last_login else None,
            "is_active": self.is_active,
            "is_admin": self.is_admin
        }
    
    def __str__(self) -> str:
        return f"User(id={self.id[:8]}, username='{self.username}', email='{self.email}')"
    
    def __repr__(self) -> str:
        return self.__str__()


class UserManager:
    """Manages a collection of users with authentication and CRUD operations."""
    
    def __init__(self):
        self._users: Dict[str, User] = {}
        self._username_index: Dict[str, str] = {}  # username -> user_id
        self._email_index: Dict[str, str] = {}     # email -> user_id
    
    def create_user(self, username: str, email: str, password: str, full_name: str = "") -> User:
        """Create a new user and add it to the manager."""
        username_lower = username.strip().lower()
        email_lower = email.strip().lower()
        
        # Check for duplicate username
        if username_lower in self._username_index:
            raise ValueError(f"Username '{username}' already exists")
        
        # Check for duplicate email
        if email_lower in self._email_index:
            raise ValueError(f"Email '{email}' already exists")
        
        user = User(username, email, password, full_name)
        self._users[user.id] = user
        self._username_index[user.username] = user.id
        self._email_index[user.email] = user.id
        
        return user
    
    def get_user(self, user_id: str) -> Optional[User]:
        """Retrieve a user by their ID."""
        return self._users.get(user_id)
    
    def get_user_by_username(self, username: str) -> Optional[User]:
        """Retrieve a user by their username."""
        user_id = self._username_index.get(username.strip().lower())
        return self._users.get(user_id) if user_id else None
    
    def get_user_by_email(self, email: str) -> Optional[User]:
        """Retrieve a user by their email."""
        user_id = self._email_index.get(email.strip().lower())
        return self._users.get(user_id) if user_id else None
    
    def authenticate(self, username_or_email: str, password: str) -> Optional[User]:
        """Authenticate a user by username/email and password."""
        # Try username first
        user = self.get_user_by_username(username_or_email)
        if not user:
            # Try email
            user = self.get_user_by_email(username_or_email)
        
        if user and user.is_active and user.check_password(password):
            user.login()
            return user
        
        return None
    
    def get_all_users(self) -> List[User]:
        """Get all users as a list."""
        return list(self._users.values())
    
    def get_active_users(self) -> List[User]:
        """Get all active users."""
        return [user for user in self._users.values() if user.is_active]
    
    def get_admin_users(self) -> List[User]:
        """Get all admin users."""
        return [user for user in self._users.values() if user.is_admin]
    
    def update_user(self, user_id: str, **kwargs) -> bool:
        """Update user properties. Returns True if successful, False if user not found."""
        user = self.get_user(user_id)
        if not user:
            return False
        
        if "email" in kwargs:
            new_email = kwargs["email"].strip().lower()
            # Check if email is already taken by another user
            existing_user_id = self._email_index.get(new_email)
            if existing_user_id and existing_user_id != user_id:
                raise ValueError(f"Email '{kwargs['email']}' already exists")
            
            # Update indexes
            del self._email_index[user.email]
            user.update_email(kwargs["email"])
            self._email_index[user.email] = user_id
        
        if "full_name" in kwargs:
            user.update_full_name(kwargs["full_name"])
        
        return True
    
    def delete_user(self, user_id: str) -> bool:
        """Delete a user by their ID. Returns True if successful, False if user not found."""
        user = self.get_user(user_id)
        if not user:
            return False
        
        # Remove from indexes
        del self._username_index[user.username]
        del self._email_index[user.email]
        del self._users[user_id]
        
        return True
    
    def count_users(self) -> int:
        """Get the total number of users."""
        return len(self._users)
    
    def clear_all_users(self) -> None:
        """Remove all users from the manager."""
        self._users.clear()
        self._username_index.clear()
        self._email_index.clear()