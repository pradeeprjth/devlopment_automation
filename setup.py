from setuptools import setup, find_packages

setup(
    name="task_manager",
    version="0.1.0",
    description="A simple task management library for testing purposes",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[],
    extras_require={
        "dev": ["pytest>=7.0.0", "pytest-cov>=4.0.0"]
    }
)