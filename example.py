"""
Example usage of the task_manager library.
"""

from task_manager import Task, TaskManager, User, UserManager
from task_manager import MathUtils, StringUtils, EmailValidator, PasswordValidator
from task_manager.task import TaskStatus, TaskPriority
from datetime import datetime, timedelta


def demo_task_management():
    """Demonstrate task management functionality."""
    print("=== Task Management Demo ===")
    
    # Create task manager
    tm = TaskManager()
    
    # Create some tasks
    task1 = tm.create_task("Complete project proposal", "Write and submit the Q4 project proposal", TaskPriority.HIGH)
    task2 = tm.create_task("Review code", "Review pull requests from team", TaskPriority.MEDIUM)
    task3 = tm.create_task("Update documentation", priority=TaskPriority.LOW)
    
    print(f"Created {tm.count_tasks()} tasks")
    
    # Update task status
    task1.update_status(TaskStatus.IN_PROGRESS)
    task2.update_status(TaskStatus.COMPLETED)
    
    # Set due date
    due_date = datetime.now() + timedelta(days=7)
    task1.set_due_date(due_date)
    
    # Get tasks by status
    pending_tasks = tm.get_tasks_by_status(TaskStatus.PENDING)
    print(f"Pending tasks: {len(pending_tasks)}")
    
    # Print all tasks
    for task in tm.get_all_tasks():
        print(f"  {task}")


def demo_user_management():
    """Demonstrate user management functionality."""
    print("\n=== User Management Demo ===")
    
    # Create user manager
    um = UserManager()
    
    # Create users
    try:
        user1 = um.create_user("john_doe", "john@example.com", "SecurePass123!", "John Doe")
        user2 = um.create_user("jane_smith", "jane@example.com", "AnotherPass456!", "Jane Smith")
        
        print(f"Created {um.count_users()} users")
        
        # Authenticate user
        authenticated_user = um.authenticate("john_doe", "SecurePass123!")
        if authenticated_user:
            print(f"Authentication successful for {authenticated_user.username}")
        
        # Make user admin
        user1.make_admin()
        print(f"Admin users: {len(um.get_admin_users())}")
        
    except ValueError as e:
        print(f"Error creating user: {e}")


def demo_math_utils():
    """Demonstrate mathematical utilities."""
    print("\n=== Math Utils Demo ===")
    
    # Factorial
    print(f"Factorial of 5: {MathUtils.factorial(5)}")
    
    # Fibonacci sequence
    fib_sequence = MathUtils.fibonacci(10)
    print(f"First 10 Fibonacci numbers: {fib_sequence}")
    
    # Prime check
    print(f"Is 17 prime? {MathUtils.is_prime(17)}")
    print(f"Is 18 prime? {MathUtils.is_prime(18)}")
    
    # GCD and LCM
    print(f"GCD of 48 and 18: {MathUtils.gcd(48, 18)}")
    print(f"LCM of 48 and 18: {MathUtils.lcm(48, 18)}")
    
    # Average and median
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    print(f"Average of {numbers}: {MathUtils.average(numbers)}")
    print(f"Median of {numbers}: {MathUtils.median(numbers)}")


def demo_string_utils():
    """Demonstrate string utilities."""
    print("\n=== String Utils Demo ===")
    
    text = "Hello, World! This is a test string with 123 numbers."
    
    print(f"Original text: {text}")
    print(f"Reversed: {StringUtils.reverse_string(text)}")
    print(f"Word count: {StringUtils.count_words(text)}")
    print(f"Vowel count: {StringUtils.count_vowels(text)}")
    print(f"Capitalized: {StringUtils.capitalize_words(text.lower())}")
    print(f"Numbers extracted: {StringUtils.extract_numbers(text)}")
    print(f"Cleaned text: {StringUtils.clean_text(text)}")
    print(f"Truncated (30 chars): {StringUtils.truncate(text, 30)}")
    
    # Palindrome check
    palindrome = "A man a plan a canal Panama"
    print(f"Is '{palindrome}' a palindrome? {StringUtils.is_palindrome(palindrome)}")


def demo_validators():
    """Demonstrate validation utilities."""
    print("\n=== Validators Demo ===")
    
    # Email validation
    emails = ["test@example.com", "invalid-email", "user@domain.co.uk"]
    for email in emails:
        valid = EmailValidator.is_valid(email)
        print(f"Email '{email}' is valid: {valid}")
        if valid:
            print(f"  Domain: {EmailValidator.get_domain(email)}")
            print(f"  Username: {EmailValidator.get_username(email)}")
    
    # Password validation
    validator = PasswordValidator()
    passwords = ["weak", "StrongPass123!", "NoDigits!", "nouppercase123!"]
    
    for password in passwords:
        strength = validator.get_strength_level(password)
        score = validator.get_strength_score(password)
        errors = validator.validate(password)
        
        print(f"Password '{password}':")
        print(f"  Strength: {strength} (Score: {score})")
        if errors:
            print(f"  Errors: {', '.join(errors)}")
        else:
            print(f"  Valid: Yes")


if __name__ == "__main__":
    demo_task_management()
    demo_user_management()
    demo_math_utils()
    demo_string_utils()
    demo_validators()
