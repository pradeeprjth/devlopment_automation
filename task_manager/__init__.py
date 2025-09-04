"""
Task Manager - A simple library for managing tasks and users.

This library provides functionality for:
- Managing tasks with priorities and statuses
- User management and authentication
- Mathematical utilities
- Data validation and processing
"""

from .task import Task, TaskManager, TaskStatus, TaskPriority
from .user import User, UserManager
from .utils import MathUtils, StringUtils
from .validators import EmailValidator, PasswordValidator

__version__ = "0.1.0"
__all__ = [
    "Task", "TaskManager", "TaskStatus", "TaskPriority",
    "User", "UserManager",
    "MathUtils", "StringUtils",
    "EmailValidator", "PasswordValidator"
]
