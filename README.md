# Task Manager Library

A comprehensive Python library for task and user management, designed to provide extensive testing opportunities for various testing scenarios.

## Overview

This project includes multiple modules with different functionalities, making it perfect for writing comprehensive test suites. You can practice testing:

- **Object-oriented classes** with state management
- **Data validation** and error handling
- **Mathematical algorithms** and edge cases
- **String processing** utilities
- **User authentication** and security
- **CRUD operations** and data persistence
- **Enum and datetime** handling

## Project Structure

```
task_manager/
├── __init__.py          # Main package initialization
├── task.py              # Task and TaskManager classes
├── user.py              # User and UserManager classes
├── utils.py             # Mathematical and string utilities
└── validators.py        # Email, password, and data validators

tests/
└── __init__.py          # Test package (ready for your test files)

example.py               # Comprehensive usage examples
pytest.ini              # Pytest configuration
requirements.txt        # Project dependencies
setup.py                # Package setup configuration
```

## Features

### Task Management (`task.py`)
- **Task class**: Create tasks with title, description, priority, and status
- **TaskManager class**: CRUD operations, filtering, and task organization
- **Enums**: TaskStatus and TaskPriority for type safety
- **DateTime handling**: Creation time, updates, due dates
- **Validation**: Input validation and error handling

### User Management (`user.py`)
- **User class**: User creation with authentication
- **UserManager class**: User CRUD, authentication, and indexing
- **Password hashing**: Secure password storage and verification
- **Duplicate prevention**: Username and email uniqueness
- **Role management**: Admin privileges and user activation

### Mathematical Utilities (`utils.py`)
- **MathUtils class**: Factorial, Fibonacci, prime checking, GCD/LCM
- **Statistical functions**: Average, median calculations
- **Number operations**: Power calculations with error handling
- **Input validation**: Type checking and edge case handling

### String Utilities (`utils.py`)
- **StringUtils class**: String manipulation and analysis
- **Text processing**: Word counting, vowel counting, palindrome checking
- **Text cleaning**: Punctuation removal, space normalization
- **Pattern extraction**: Number extraction from text
- **Text transformation**: Capitalization, truncation, deduplication

### Validation Tools (`validators.py`)
- **EmailValidator**: Email format validation and domain extraction
- **PasswordValidator**: Configurable password strength checking
- **DataValidator**: Phone numbers, URLs, and general data validation
- **Security features**: Input sanitization and length limits

## Installation

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Install the package in development mode:
```bash
pip install -e .
```

## Usage

Run the example script to see all features in action:
```bash
python example.py
```

## Testing Opportunities

This library provides excellent opportunities to practice writing tests for:

### Unit Testing Scenarios
1. **Constructor validation** - Test object creation with valid/invalid inputs
2. **Method behavior** - Test individual method functionality
3. **State management** - Test object state changes over time
4. **Error conditions** - Test exception handling and error messages
5. **Edge cases** - Test boundary conditions and special values
6. **Type checking** - Test input type validation

### Integration Testing Scenarios
1. **Manager classes** - Test interactions between objects and their managers
2. **Authentication flows** - Test user creation, login, and permission systems
3. **Task workflows** - Test complete task lifecycle management
4. **Data consistency** - Test data integrity across operations

### Test Categories to Implement

#### Task Management Tests
- Task creation with various inputs
- Task status transitions
- Due date validation and overdue detection
- Task assignment and filtering
- TaskManager CRUD operations
- Bulk operations and error handling

#### User Management Tests
- User registration with duplicate checking
- Password hashing and verification
- Authentication with various credentials
- User role management
- Email and username uniqueness
- User deactivation and reactivation

#### Mathematical Utilities Tests
- Factorial calculations (including edge cases like 0! and large numbers)
- Fibonacci sequence generation
- Prime number detection
- GCD and LCM calculations
- Statistical functions with various datasets
- Error handling for invalid inputs

#### String Utilities Tests
- String reversal and palindrome detection
- Word and character counting
- Text cleaning and sanitization
- Pattern extraction and matching
- Text transformation functions
- Unicode and special character handling

#### Validation Tests
- Email format validation with various patterns
- Password strength evaluation
- Phone number format validation
- URL validation
- Input sanitization effectiveness

### Testing Best Practices to Practice
1. **Arrange-Act-Assert** pattern
2. **Test isolation** and independence
3. **Parameterized tests** for multiple inputs
4. **Mock objects** for external dependencies
5. **Test fixtures** for common setup
6. **Exception testing** with pytest.raises
7. **Coverage analysis** to ensure comprehensive testing
8. **Performance testing** for algorithmic functions

## Getting Started with Testing

1. Create test files in the `tests/` directory
2. Use pytest for running tests: `pytest tests/`
3. Generate coverage reports: `pytest --cov=task_manager tests/`
4. Run specific test categories: `pytest -m unit tests/`

## Example Test Structure

```python
# tests/test_task.py
import pytest
from task_manager import Task, TaskManager, TaskStatus, TaskPriority

class TestTask:
    def test_task_creation_valid_input(self):
        # Test successful task creation
        pass
    
    def test_task_creation_invalid_input(self):
        # Test task creation with invalid inputs
        pass
    
    def test_task_status_update(self):
        # Test status transitions
        pass
    
    # Add more test methods...

class TestTaskManager:
    def setup_method(self):
        # Setup for each test method
        self.task_manager = TaskManager()
    
    def test_create_task(self):
        # Test task creation through manager
        pass
    
    # Add more test methods...
```

This project structure provides a rich foundation for exploring different testing patterns, scenarios, and best practices in Python development!