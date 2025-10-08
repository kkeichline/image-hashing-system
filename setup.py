from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="image-hash-system",
    version="1.0.0",
    author="Your Name",  # TODO: Update with your name
    author_email="your.email@example.com",  # TODO: Update with your email
    description="Privacy-preserving image similarity detection system",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/image-hash-system",  # TODO: Update URL
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=[
        "imagehash>=4.3.1",
        "Pillow>=10.2.0",
        "sqlalchemy>=2.0.25",
        "psycopg2-binary>=2.9.9",
        "fastapi>=0.109.0",
        "uvicorn>=0.27.0",
        "pydantic>=2.5.3",
        "click>=8.1.7",
        "numpy>=1.26.3",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.4",
            "pytest-asyncio>=0.23.3",
            "httpx>=0.26.0",
            "black>=24.1.1",
            "flake8>=7.0.0",
            "mypy>=1.8.0",
        ],
        "cache": [
            "redis>=5.0.1",
        ],
    },
    entry_points={
        "console_scripts": [
            "image-hash=cli.commands:cli",
        ],
    },
)
