#!/bin/bash

echo "=== Installing compatible Gemini API version ==="
pip install google-generativeai==0.1.0rc1

echo "=== Testing AI functionality ==="
python debug_ai.py

echo "=== Testing full bot (background) ==="
nohup python bloomberg_simple.py &

echo "=== Setup complete! ==="
echo "Bot is now running in background"
echo "AI analysis should work with the legacy API fallback"
