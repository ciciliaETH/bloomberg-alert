#!/bin/bash
# Fix script untuk upgrade google-generativeai di VPS

echo "🔧 FIXING GOOGLE-GENERATIVEAI VERSION"
echo "======================================"

# Check if we're in the right directory
if [ ! -f "bloomberg_simple.py" ]; then
    echo "❌ Not in Bloomberg bot directory!"
    echo "Please run this from ~/bloomberg-bot/ or move to correct directory"
    exit 1
fi

# Check for virtual environment
if [ -d "venv" ]; then
    echo "✅ Found virtual environment"
    source venv/bin/activate
else
    echo "❌ Virtual environment not found!"
    echo "Creating new virtual environment..."
    python3 -m venv venv
    source venv/bin/activate
fi

echo "📦 Current google-generativeai version:"
pip show google-generativeai || echo "Not installed"

echo "🗑️ Uninstalling old version..."
pip uninstall google-generativeai -y || true

echo "📥 Installing compatible version for Python 3.8..."
# Try different versions that work with Python 3.8
pip install google-generativeai --pre --upgrade || \
pip install google-generativeai==0.3.2 || \
pip install google-generativeai==0.2.2 || \
pip install google-generativeai

echo "✅ Installed version:"
pip show google-generativeai

echo "🧪 Testing new installation..."
python3 -c "
import google.generativeai as genai
print('✅ google.generativeai imported successfully')
print('GenerativeModel available:', hasattr(genai, 'GenerativeModel'))
if hasattr(genai, 'GenerativeModel'):
    print('✅ GenerativeModel class found!')
else:
    print('❌ GenerativeModel class not found - using legacy API')
"

echo "🔄 Running debug test..."
if [ -f "debug_ai.py" ]; then
    python3 debug_ai.py
else
    echo "❌ debug_ai.py not found"
fi

echo "✅ Fix completed!"
