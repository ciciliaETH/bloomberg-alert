#!/bin/bash
# GitHub Codespaces startup script

echo "🚀 Starting Bloomberg Alert Bot in GitHub Codespaces..."

# Setup environment variables
export TELEGRAM_TOKEN="8122220616:AAFI8xFd2O0X1UiJWBWvO8j5-pgeysLCbpc"
export GEMINI_API_KEY="AIzaSyAPYV-zu5bNVFcTeElaXYWokZEk_wlAWms"

# Note: GOOGLE_CREDENTIALS_JSON perlu di-set manual di Codespaces Secrets

echo "✅ Environment variables set"
echo "📧 Make sure to add GOOGLE_CREDENTIALS_JSON to Codespaces Secrets"
echo ""
echo "To run the bot:"
echo "python bloomberg_simple.py"
