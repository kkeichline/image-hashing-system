#!/bin/bash

# Development Environment Setup Script
# This script helps set up your development environment

set -e  # Exit on error

echo "🚀 Image Hash System - Development Setup"
echo "========================================"
echo ""

# Check Python version
echo "📋 Checking Python version..."
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "   Found Python $python_version"

# Check if Python 3.8+
required_version="3.8"
if [ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]; then 
    echo "❌ Error: Python 3.8+ is required"
    exit 1
fi
echo "   ✅ Python version OK"
echo ""

# Create virtual environment
echo "🔧 Creating virtual environment..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo "   ✅ Virtual environment created"
else
    echo "   ℹ️  Virtual environment already exists"
fi
echo ""

# Activate virtual environment
echo "🔌 Activating virtual environment..."
source venv/bin/activate
echo "   ✅ Virtual environment activated"
echo ""

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip > /dev/null 2>&1
echo "   ✅ pip upgraded"
echo ""

# Install dependencies
echo "📦 Installing dependencies..."
echo "   This may take a few minutes..."
pip install -r requirements.txt > /dev/null 2>&1
echo "   ✅ Dependencies installed"
echo ""

# Check if PostgreSQL is available
echo "🔍 Checking for PostgreSQL..."
if command -v psql &> /dev/null; then
    echo "   ✅ PostgreSQL found"
    echo "   You can create a database with: createdb image_hashes"
else
    echo "   ⚠️  PostgreSQL not found"
    echo "   No problem! You can use SQLite for development"
fi
echo ""

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cat > .env << 'EOL'
# Database Configuration
# For SQLite (development):
DATABASE_URL=sqlite:///image_hashes.db

# For PostgreSQL (production):
# DATABASE_URL=postgresql://localhost/image_hashes

# Optional: Redis cache
# REDIS_URL=redis://localhost:6379

# API Configuration
API_HOST=0.0.0.0
API_PORT=8000
EOL
    echo "   ✅ .env file created"
else
    echo "   ℹ️  .env file already exists"
fi
echo ""

# Create sample images directory
mkdir -p data/sample_images
echo "📁 Directory structure ready"
echo ""

# Run a quick test
echo "🧪 Running quick health check..."
python3 << 'EOF'
try:
    import imagehash
    import PIL
    import sqlalchemy
    import fastapi
    import click
    print("   ✅ All core packages imported successfully")
except ImportError as e:
    print(f"   ❌ Error importing packages: {e}")
    exit(1)
EOF
echo ""

# Summary
echo "✨ Setup Complete!"
echo "=================="
echo ""
echo "📚 Next Steps:"
echo ""
echo "1. Review the implementation guide:"
echo "   open GETTING_STARTED.md"
echo ""
echo "2. Start with Phase 1 (Hash Generation):"
echo "   code src/hasher/generator.py"
echo ""
echo "3. Test your implementation:"
echo "   python3 -c 'from src.hasher.generator import ImageHasher; print(\"Import works!\")'"
echo ""
echo "4. When ready, start the API server:"
echo "   python -m uvicorn src.api.main:app --reload"
echo ""
echo "5. Run tests:"
echo "   pytest tests/ -v"
echo ""
echo "📖 Documentation:"
echo "   - GETTING_STARTED.md - Implementation guide"
echo "   - docs/ARCHITECTURE.md - System design"
echo "   - docs/API.md - API documentation"
echo "   - docs/ETHICS.md - ⚠️ IMPORTANT: Read this!"
echo ""
echo "💡 Pro tip: Keep your virtual environment activated:"
echo "   source venv/bin/activate"
echo ""
echo "Happy coding! 🚀"
