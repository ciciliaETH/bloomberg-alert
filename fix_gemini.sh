#!/bin/bash
# Fix script untuk upgrade google-generativeai di VPS

echo "🔧 FIXING GOOGLE-GENERATIVEAI VERSION"
echo "======================================"

# Activate virtual environment
source venv/bin/activate

echo "📦 Current google-generativeai version:"
pip show google-generativeai || echo "Not installed"

echo "🗑️ Uninstalling old version..."
pip uninstall google-generativeai -y

echo "📥 Installing latest version..."
pip install "google-generativeai>=0.8.0" --upgrade

echo "✅ New version installed:"
pip show google-generativeai

echo "🧪 Testing new installation..."
python3 -c "import google.generativeai as genai; print('GenerativeModel available:', hasattr(genai, 'GenerativeModel'))"

echo "🔄 Running debug test..."
python3 debug_ai.py

echo "✅ Fix completed!"
