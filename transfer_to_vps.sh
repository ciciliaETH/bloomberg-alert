#!/bin/bash
# Quick file transfer to VPS
# Usage: bash transfer_to_vps.sh your-server-ip

if [ -z "$1" ]; then
    echo "Usage: bash transfer_to_vps.sh your-server-ip"
    exit 1
fi

VPS_IP=$1
VPS_USER=${2:-ubuntu}  # default user ubuntu

echo "📦 Transferring files to VPS..."

# Create directory on VPS
ssh $VPS_USER@$VPS_IP "mkdir -p ~/bloomberg-bot"

# Transfer essential files
scp token.json $VPS_USER@$VPS_IP:~/bloomberg-bot/
scp credentials.json $VPS_USER@$VPS_IP:~/bloomberg-bot/
scp .env.production $VPS_USER@$VPS_IP:~/bloomberg-bot/.env

echo "✅ Files transferred!"
echo ""
echo "Now SSH to your VPS and run:"
echo "cd ~/bloomberg-bot && bash deploy.sh"
