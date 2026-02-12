#!/bin/bash
# CropGuard AI - Setup and Deployment Script

echo "🌾 CropGuard AI - Setup Script"
echo "=============================="

# Check Python installation
echo "📌 Checking Python installation..."
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo "✓ Python found: $PYTHON_VERSION"
else
    echo "✗ Python 3 not found. Please install Python 3.8 or higher"
    exit 1
fi

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔄 Activating virtual environment..."
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    source venv/Scripts/activate
else
    source venv/bin/activate
fi

# Upgrade pip
echo ""
echo "⬆️  Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create necessary directories
echo ""
echo "📁 Creating necessary directories..."
mkdir -p database
mkdir -p frontend/static/uploads
mkdir -p models

# Initialize database
echo ""
echo "💾 Initializing database..."
cd backend
python3 << EOF
from app import app, db
with app.app_context():
    db.create_all()
    print("✓ Database initialized successfully")
EOF
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "🚀 To run the application:"
echo "   1. Activate virtual environment:"
echo "      - Windows: venv\\Scripts\\activate"
echo "      - Mac/Linux: source venv/bin/activate"
echo "   2. Run the application:"
echo "      cd backend && python app.py"
echo "   3. Open browser and navigate to:"
echo "      http://localhost:5000"
echo ""
echo "📚 For more information, see README.md"
