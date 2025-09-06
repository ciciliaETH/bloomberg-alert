#!/bin/bash

echo "=== Ubuntu 20.04 VPS Setup for Bloomberg Bot ==="

# Check current environment
echo "📋 System Info:"
echo "OS: $(lsb_release -d | cut -f2)"
echo "Python: $(python3 --version)"
echo "Pip: $(pip3 --version)"

# Update system
echo "📦 Updating system..."
sudo apt update && sudo apt upgrade -y

# Install Python essentials
echo "🐍 Installing Python dependencies..."
sudo apt install python3-pip python3-venv python3-dev build-essential -y

# Navigate to project directory
cd ~/bloomberg-alert || { echo "Directory not found"; exit 1; }

# Create virtual environment with Python 3.8 compatible packages
echo "🔧 Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Install specific versions for Ubuntu 20.04 + Python 3.8
echo "📦 Installing compatible packages..."

# Core packages first
pip install --upgrade pip setuptools wheel

# Google packages with specific versions for Python 3.8
pip install google-auth==2.23.0
pip install google-auth-oauthlib==1.0.0
pip install google-auth-httplib2==0.1.1
pip install google-api-python-client==2.100.0

# Try different Gemini AI versions
echo "🤖 Installing Google Generative AI..."
pip install google-generativeai==0.3.2 || \
pip install google-generativeai==0.2.2 || \
pip install google-generativeai==0.1.0 || \
echo "All Gemini versions failed, will use alternative"

# Other dependencies
pip install requests==2.31.0
pip install urllib3==1.26.18

echo "📋 Final package list:"
pip list | grep -E "(google|requests)"

echo "✅ Setup complete!"
echo "📝 Activate with: source venv/bin/activate"
