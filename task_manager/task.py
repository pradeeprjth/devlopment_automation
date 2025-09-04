"""
Task management module providing Task and TaskManager classes.
"""

from datetime import datetime
from enum import Enum
from typing import List, Optional, Dict, Any
import uuid


class TaskStatus(Enum):
    """Enumeration for task statuses."""
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TaskPriority(Enum):
    """Enumeration for task priorities."""
    LOW = 1
    MEDIUM = 2
    HIGH = 3
    URGENT = 4


class Task:
    """Represents a single task with title, description, priority, and status."""
    
    def __init__(self, title: str, description: str = "", priority: TaskPriority = TaskPriority.MEDIUM):
        if not title or not title.strip():
            raise ValueError("Task title cannot be empty")
        
        self.id = str(uuid.uuid4())
        self.title = title.strip()
        self.description = description.strip()
        self.priority = priority
        self.status = TaskStatus.PENDING
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.due_date: Optional[datetime] = None
        self.assigned_to: Optional[str] = None
    
    def update_status(self, status: TaskStatus) -> None:
        """Update the task status and update timestamp."""
        if not isinstance(status, TaskStatus):
            raise ValueError("Status must be a TaskStatus enum value")
        
        self.status = status
        self.updated_at = datetime.now()
    
    def set_due_date(self, due_date: datetime) -> None:
        """Set the due date for the task."""
        if due_date < datetime.now():
            raise ValueError("Due date cannot be in the past")
        
        self.due_date = due_date
        self.updated_at = datetime.now()
    
    def assign_to(self, user_id: str) -> None:
        """Assign the task to a user."""
        if not user_id or not user_id.strip():
            raise ValueError("User ID cannot be empty")
        
        self.assigned_to = user_id.strip()
        self.updated_at = datetime.now()
    
    def is_overdue(self) -> bool:
        """Check if the task is overdue."""
        if self.due_date is None:
            return False
        return datetime.now() > self.due_date and self.status != TaskStatus.COMPLETED
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary representation."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "priority": self.priority.name,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "assigned_to": self.assigned_to
        }
    
    def __str__(self) -> str:
        return f"Task(id={self.id[:8]}, title='{self.title}', status={self.status.value})"
    
    def __repr__(self) -> str:
        return self.__str__()


class TaskManager:
    """Manages a collection of tasks with CRUD operations."""
    
    def __init__(self):
        self._tasks: Dict[str, Task] = {}
    
    def create_task(self, title: str, description: str = "", priority: TaskPriority = TaskPriority.MEDIUM) -> Task:
        """Create a new task and add it to the manager."""
        task = Task(title, description, priority)
        self._tasks[task.id] = task
        return task
    
    def get_task(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by its ID."""
        return self._tasks.get(task_id)
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks as a list."""
        return list(self._tasks.values())
    
    def update_task(self, task_id: str, **kwargs) -> bool:
        """Update task properties. Returns True if successful, False if task not found."""
        task = self.get_task(task_id)
        if not task:
            return False
        
        if "title" in kwargs:
            if not kwargs["title"] or not kwargs["title"].strip():
                raise ValueError("Task title cannot be empty")
            task.title = kwargs["title"].strip()
        
        if "description" in kwargs:
            task.description = kwargs["description"].strip()
        
        if "priority" in kwargs:
            if not isinstance(kwargs["priority"], TaskPriority):
                raise ValueError("Priority must be a TaskPriority enum value")
            task.priority = kwargs["priority"]
        
        task.updated_at = datetime.now()
        return True
    
    def delete_task(self, task_id: str) -> bool:
        """Delete a task by its ID. Returns True if successful, False if task not found."""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False
    
    def get_tasks_by_status(self, status: TaskStatus) -> List[Task]:
        """Get all tasks with a specific status."""
        return [task for task in self._tasks.values() if task.status == status]
    
    def get_tasks_by_priority(self, priority: TaskPriority) -> List[Task]:
        """Get all tasks with a specific priority."""
        return [task for task in self._tasks.values() if task.priority == priority]
    
    def get_overdue_tasks(self) -> List[Task]:
        """Get all overdue tasks."""
        return [task for task in self._tasks.values() if task.is_overdue()]
    
    def get_tasks_assigned_to(self, user_id: str) -> List[Task]:
        """Get all tasks assigned to a specific user."""
        return [task for task in self._tasks.values() if task.assigned_to == user_id]
    
    def count_tasks(self) -> int:
        """Get the total number of tasks."""
        return len(self._tasks)
    
    def clear_all_tasks(self) -> None:
        """Remove all tasks from the manager."""
        self._tasks.clear()
