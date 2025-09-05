#!/bin/bash
# VPS Setup Script untuk Bloomberg Alert Bot
# Run dengan: bash vps_setup.sh

echo "🚀 Setting up Bloomberg Alert Bot on VPS..."

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3 (available version) dan pip
sudo apt install python3 python3-pip python3-venv git curl -y

# Check Python version
echo "📋 Python version installed:"
python3 --version

# Create application directory
mkdir -p ~/bloomberg-bot
cd ~/bloomberg-bot

# Clone repository
git clone https://github.com/ciciliaETH/bloomberg-alert.git .

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

echo "✅ Basic setup completed!"
echo ""
echo "Next steps:"
echo "1. Setup environment variables: nano .env"
echo "2. Upload token.json and credentials.json"
echo "3. Run: python bloomberg_simple.py"
