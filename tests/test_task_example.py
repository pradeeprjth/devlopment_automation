"""
Sample test file demonstrating how to write tests for the task_manager library.
This serves as a template and example for writing comprehensive test suites.
"""

import pytest
from datetime import datetime, timedelta
from task_manager import Task, TaskManager, TaskStatus, TaskPriority


class TestTask:
    """Test cases for the Task class."""
    
    def test_task_creation_with_valid_inputs(self):
        """Test creating a task with valid inputs."""
        task = Task("Test Task", "This is a test description", TaskPriority.HIGH)
        
        assert task.title == "Test Task"
        assert task.description == "This is a test description"
        assert task.priority == TaskPriority.HIGH
        assert task.status == TaskStatus.PENDING
        assert task.id is not None
        assert task.created_at is not None
        assert task.updated_at is not None
        assert task.due_date is None
        assert task.assigned_to is None
    
    def test_task_creation_with_empty_title_raises_error(self):
        """Test that creating a task with empty title raises ValueError."""
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task("")
        
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            Task("   ")  # Only whitespace
    
    def test_task_status_update(self):
        """Test updating task status."""
        task = Task("Test Task")
        original_updated_time = task.updated_at
        
        # Small delay to ensure timestamp changes
        import time
        time.sleep(0.001)
        
        task.update_status(TaskStatus.IN_PROGRESS)
        
        assert task.status == TaskStatus.IN_PROGRESS
        assert task.updated_at > original_updated_time
    
    def test_task_status_update_with_invalid_status_raises_error(self):
        """Test that updating status with invalid type raises ValueError."""
        task = Task("Test Task")
        
        with pytest.raises(ValueError, match="Status must be a TaskStatus enum value"):
            task.update_status("invalid_status")
    
    def test_set_due_date_valid(self):
        """Test setting a valid due date."""
        task = Task("Test Task")
        future_date = datetime.now() + timedelta(days=7)
        
        task.set_due_date(future_date)
        
        assert task.due_date == future_date
    
    def test_set_due_date_in_past_raises_error(self):
        """Test that setting due date in the past raises ValueError."""
        task = Task("Test Task")
        past_date = datetime.now() - timedelta(days=1)
        
        with pytest.raises(ValueError, match="Due date cannot be in the past"):
            task.set_due_date(past_date)
    
    def test_assign_task_to_user(self):
        """Test assigning task to a user."""
        task = Task("Test Task")
        user_id = "user123"
        
        task.assign_to(user_id)
        
        assert task.assigned_to == user_id
    
    def test_assign_task_with_empty_user_id_raises_error(self):
        """Test that assigning with empty user ID raises ValueError."""
        task = Task("Test Task")
        
        with pytest.raises(ValueError, match="User ID cannot be empty"):
            task.assign_to("")
        
        with pytest.raises(ValueError, match="User ID cannot be empty"):
            task.assign_to("   ")
    
    def test_is_overdue_with_no_due_date(self):
        """Test overdue check when no due date is set."""
        task = Task("Test Task")
        
        assert not task.is_overdue()
    
    def test_is_overdue_with_future_due_date(self):
        """Test overdue check with future due date."""
        task = Task("Test Task")
        future_date = datetime.now() + timedelta(days=1)
        task.set_due_date(future_date)
        
        assert not task.is_overdue()
    
    def test_is_overdue_with_completed_task(self):
        """Test that completed tasks are never overdue."""
        task = Task("Test Task")
        past_date = datetime.now() - timedelta(days=1)
        # We need to manually set this for testing purposes
        task.due_date = past_date
        task.update_status(TaskStatus.COMPLETED)
        
        assert not task.is_overdue()
    
    def test_task_to_dict(self):
        """Test converting task to dictionary."""
        task = Task("Test Task", "Description", TaskPriority.HIGH)
        task_dict = task.to_dict()
        
        expected_keys = {
            "id", "title", "description", "priority", "status",
            "created_at", "updated_at", "due_date", "assigned_to"
        }
        
        assert set(task_dict.keys()) == expected_keys
        assert task_dict["title"] == "Test Task"
        assert task_dict["description"] == "Description"
        assert task_dict["priority"] == "HIGH"
        assert task_dict["status"] == "pending"


class TestTaskManager:
    """Test cases for the TaskManager class."""
    
    def setup_method(self):
        """Set up a fresh TaskManager for each test."""
        self.task_manager = TaskManager()
    
    def test_create_task(self):
        """Test creating a task through the manager."""
        task = self.task_manager.create_task("New Task", "Description", TaskPriority.LOW)
        
        assert task.title == "New Task"
        assert task.description == "Description"
        assert task.priority == TaskPriority.LOW
        assert self.task_manager.count_tasks() == 1
        assert self.task_manager.get_task(task.id) == task
    
    def test_get_task_existing(self):
        """Test retrieving an existing task."""
        task = self.task_manager.create_task("Test Task")
        retrieved_task = self.task_manager.get_task(task.id)
        
        assert retrieved_task == task
    
    def test_get_task_nonexistent(self):
        """Test retrieving a non-existent task returns None."""
        result = self.task_manager.get_task("nonexistent_id")
        
        assert result is None
    
    def test_get_all_tasks(self):
        """Test getting all tasks."""
        task1 = self.task_manager.create_task("Task 1")
        task2 = self.task_manager.create_task("Task 2")
        
        all_tasks = self.task_manager.get_all_tasks()
        
        assert len(all_tasks) == 2
        assert task1 in all_tasks
        assert task2 in all_tasks
    
    def test_update_task_existing(self):
        """Test updating an existing task."""
        task = self.task_manager.create_task("Original Title")
        
        result = self.task_manager.update_task(
            task.id, 
            title="Updated Title",
            description="New description",
            priority=TaskPriority.URGENT
        )
        
        assert result is True
        assert task.title == "Updated Title"
        assert task.description == "New description"
        assert task.priority == TaskPriority.URGENT
    
    def test_update_task_nonexistent(self):
        """Test updating a non-existent task returns False."""
        result = self.task_manager.update_task("nonexistent_id", title="New Title")
        
        assert result is False
    
    def test_update_task_with_empty_title_raises_error(self):
        """Test updating task with empty title raises ValueError."""
        task = self.task_manager.create_task("Original Title")
        
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            self.task_manager.update_task(task.id, title="")
    
    def test_delete_task_existing(self):
        """Test deleting an existing task."""
        task = self.task_manager.create_task("Task to Delete")
        
        result = self.task_manager.delete_task(task.id)
        
        assert result is True
        assert self.task_manager.count_tasks() == 0
        assert self.task_manager.get_task(task.id) is None
    
    def test_delete_task_nonexistent(self):
        """Test deleting a non-existent task returns False."""
        result = self.task_manager.delete_task("nonexistent_id")
        
        assert result is False
    
    def test_get_tasks_by_status(self):
        """Test filtering tasks by status."""
        task1 = self.task_manager.create_task("Task 1")
        task2 = self.task_manager.create_task("Task 2")
        task1.update_status(TaskStatus.COMPLETED)
        
        pending_tasks = self.task_manager.get_tasks_by_status(TaskStatus.PENDING)
        completed_tasks = self.task_manager.get_tasks_by_status(TaskStatus.COMPLETED)
        
        assert len(pending_tasks) == 1
        assert len(completed_tasks) == 1
        assert task2 in pending_tasks
        assert task1 in completed_tasks
    
    def test_get_tasks_by_priority(self):
        """Test filtering tasks by priority."""
        task1 = self.task_manager.create_task("Task 1", priority=TaskPriority.HIGH)
        task2 = self.task_manager.create_task("Task 2", priority=TaskPriority.LOW)
        
        high_priority_tasks = self.task_manager.get_tasks_by_priority(TaskPriority.HIGH)
        low_priority_tasks = self.task_manager.get_tasks_by_priority(TaskPriority.LOW)
        
        assert len(high_priority_tasks) == 1
        assert len(low_priority_tasks) == 1
        assert task1 in high_priority_tasks
        assert task2 in low_priority_tasks
    
    def test_count_tasks(self):
        """Test counting tasks."""
        assert self.task_manager.count_tasks() == 0
        
        self.task_manager.create_task("Task 1")
        assert self.task_manager.count_tasks() == 1
        
        self.task_manager.create_task("Task 2")
        assert self.task_manager.count_tasks() == 2
    
    def test_clear_all_tasks(self):
        """Test clearing all tasks."""
        self.task_manager.create_task("Task 1")
        self.task_manager.create_task("Task 2")
        
        self.task_manager.clear_all_tasks()
        
        assert self.task_manager.count_tasks() == 0
        assert len(self.task_manager.get_all_tasks()) == 0


# Pytest fixtures example (uncomment to use)
@pytest.fixture
def sample_task():
    """Fixture that provides a sample task for testing."""
    return Task("Sample Task", "Sample description", TaskPriority.MEDIUM)


@pytest.fixture
def task_manager_with_tasks():
    """Fixture that provides a TaskManager with some pre-created tasks."""
    tm = TaskManager()
    tm.create_task("Task 1", "Description 1", TaskPriority.HIGH)
    tm.create_task("Task 2", "Description 2", TaskPriority.LOW)
    tm.create_task("Task 3", "Description 3", TaskPriority.MEDIUM)
    return tm


# Parametrized test example
@pytest.mark.parametrize("title,expected_valid", [
    ("Valid Title", True),
    ("", False),
    ("   ", False),
    ("A" * 100, True),  # Long but valid title
])
def test_task_title_validation(title, expected_valid):
    """Parametrized test for task title validation."""
    if expected_valid:
        task = Task(title)
        assert task.title == title.strip()
    else:
        with pytest.raises(ValueError):
            Task(title)
