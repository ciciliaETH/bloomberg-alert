#!/bin/bash
# Deploy script untuk production VPS
# Run dengan: bash deploy.sh

echo "🚀 Deploying Bloomberg Alert Bot..."

# Activate virtual environment
source venv/bin/activate

# Pull latest changes
git pull origin main

# Install/update dependencies
pip install -r requirements.txt

# Copy environment file
if [ ! -f .env ]; then
    cp .env.production .env
    echo "⚠️  Please edit .env file with your credentials"
fi

# Copy service file
if [ ! -f /etc/systemd/system/bloomberg-bot.service ]; then
    sudo cp bloomberg-bot.service /etc/systemd/system/
    sudo systemctl daemon-reload
    sudo systemctl enable bloomberg-bot
    echo "✅ Service installed and enabled"
fi

# Start/restart service
sudo systemctl restart bloomberg-bot
sudo systemctl status bloomberg-bot

echo ""
echo "✅ Deployment completed!"
echo ""
echo "Useful commands:"
echo "• Check status: sudo systemctl status bloomberg-bot"
echo "• View logs: sudo journalctl -u bloomberg-bot -f"
echo "• Stop bot: sudo systemctl stop bloomberg-bot"
echo "• Start bot: sudo systemctl start bloomberg-bot"
