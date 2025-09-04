"""
Utility modules providing mathematical and string operations.
"""

import re
import math
from typing import List, Union, Optional


class MathUtils:
    """Mathematical utility functions for common operations."""
    
    @staticmethod
    def factorial(n: int) -> int:
        """Calculate the factorial of a non-negative integer."""
        if not isinstance(n, int):
            raise TypeError("Input must be an integer")
        if n < 0:
            raise ValueError("Factorial is not defined for negative numbers")
        
        if n == 0 or n == 1:
            return 1
        
        result = 1
        for i in range(2, n + 1):
            result *= i
        return result
    
    @staticmethod
    def fibonacci(n: int) -> List[int]:
        """Generate the first n numbers in the Fibonacci sequence."""
        if not isinstance(n, int):
            raise TypeError("Input must be an integer")
        if n < 0:
            raise ValueError("Number of terms cannot be negative")
        
        if n == 0:
            return []
        elif n == 1:
            return [0]
        elif n == 2:
            return [0, 1]
        
        sequence = [0, 1]
        for i in range(2, n):
            sequence.append(sequence[i-1] + sequence[i-2])
        
        return sequence
    
    @staticmethod
    def is_prime(n: int) -> bool:
        """Check if a number is prime."""
        if not isinstance(n, int):
            raise TypeError("Input must be an integer")
        if n < 2:
            return False
        
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
    
    @staticmethod
    def gcd(a: int, b: int) -> int:
        """Calculate the Greatest Common Divisor of two integers."""
        if not isinstance(a, int) or not isinstance(b, int):
            raise TypeError("Both inputs must be integers")
        
        a, b = abs(a), abs(b)
        while b:
            a, b = b, a % b
        return a
    
    @staticmethod
    def lcm(a: int, b: int) -> int:
        """Calculate the Least Common Multiple of two integers."""
        if a == 0 or b == 0:
            return 0
        return abs(a * b) // MathUtils.gcd(a, b)
    
    @staticmethod
    def power(base: Union[int, float], exponent: Union[int, float]) -> Union[int, float]:
        """Calculate base raised to the power of exponent."""
        if not isinstance(base, (int, float)) or not isinstance(exponent, (int, float)):
            raise TypeError("Both base and exponent must be numbers")
        
        return base ** exponent
    
    @staticmethod
    def average(numbers: List[Union[int, float]]) -> float:
        """Calculate the average of a list of numbers."""
        if not numbers:
            raise ValueError("Cannot calculate average of empty list")
        
        if not all(isinstance(x, (int, float)) for x in numbers):
            raise TypeError("All items in the list must be numbers")
        
        return sum(numbers) / len(numbers)
    
    @staticmethod
    def median(numbers: List[Union[int, float]]) -> Union[int, float]:
        """Calculate the median of a list of numbers."""
        if not numbers:
            raise ValueError("Cannot calculate median of empty list")
        
        if not all(isinstance(x, (int, float)) for x in numbers):
            raise TypeError("All items in the list must be numbers")
        
        sorted_numbers = sorted(numbers)
        n = len(sorted_numbers)
        
        if n % 2 == 0:
            return (sorted_numbers[n//2 - 1] + sorted_numbers[n//2]) / 2
        else:
            return sorted_numbers[n//2]


class StringUtils:
    """String utility functions for common text operations."""
    
    @staticmethod
    def reverse_string(text: str) -> str:
        """Reverse a string."""
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        return text[::-1]
    
    @staticmethod
    def is_palindrome(text: str, ignore_case: bool = True, ignore_spaces: bool = True) -> bool:
        """Check if a string is a palindrome."""
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        
        processed_text = text
        if ignore_case:
            processed_text = processed_text.lower()
        if ignore_spaces:
            processed_text = processed_text.replace(" ", "")
        
        return processed_text == processed_text[::-1]
    
    @staticmethod
    def count_words(text: str) -> int:
        """Count the number of words in a string."""
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        
        words = text.strip().split()
        return len(words)
    
    @staticmethod
    def count_vowels(text: str) -> int:
        """Count the number of vowels in a string."""
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        
        vowels = "aeiouAEIOU"
        return sum(1 for char in text if char in vowels)
    
    @staticmethod
    def capitalize_words(text: str) -> str:
        """Capitalize the first letter of each word."""
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        
        return ' '.join(word.capitalize() for word in text.split())
    
    @staticmethod
    def remove_duplicates(text: str, preserve_order: bool = True) -> str:
        """Remove duplicate characters from a string."""
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        
        if preserve_order:
            seen = set()
            result = []
            for char in text:
                if char not in seen:
                    seen.add(char)
                    result.append(char)
            return ''.join(result)
        else:
            return ''.join(set(text))
    
    @staticmethod
    def extract_numbers(text: str) -> List[int]:
        """Extract all numbers from a string."""
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        
        numbers = re.findall(r'-?\d+', text)
        return [int(num) for num in numbers]
    
    @staticmethod
    def clean_text(text: str, remove_punctuation: bool = True, 
                  remove_extra_spaces: bool = True) -> str:
        """Clean text by removing punctuation and/or extra spaces."""
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        
        result = text
        
        if remove_punctuation:
            result = re.sub(r'[^\w\s]', '', result)
        
        if remove_extra_spaces:
            result = re.sub(r'\s+', ' ', result).strip()
        
        return result
    
    @staticmethod
    def truncate(text: str, max_length: int, suffix: str = "...") -> str:
        """Truncate text to a maximum length with an optional suffix."""
        if not isinstance(text, str):
            raise TypeError("Input must be a string")
        if not isinstance(max_length, int):
            raise TypeError("Max length must be an integer")
        if max_length < 0:
            raise ValueError("Max length cannot be negative")
        
        if len(text) <= max_length:
            return text
        
        if len(suffix) >= max_length:
            return text[:max_length]
        
        return text[:max_length - len(suffix)] + suffix
