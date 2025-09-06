#!/bin/bash

echo "=== Stopping Bloomberg Bot ==="

# Method 1: Kill by name
echo "🔄 Killing bloomberg_simple.py processes..."
pkill -f bloomberg_simple.py

# Wait a moment
sleep 2

# Check if still running
if pgrep -f bloomberg_simple.py > /dev/null; then
    echo "⚠️ Process still running, force killing..."
    # Method 2: Force kill
    pkill -9 -f bloomberg_simple.py
    sleep 1
fi

# Final check
if pgrep -f bloomberg_simple.py > /dev/null; then
    echo "❌ Failed to stop bot, showing remaining processes:"
    ps aux | grep bloomberg
else
    echo "✅ Bot stopped successfully!"
fi

echo "=== Bot Status ==="
echo "Running processes:"
ps aux | grep -v grep | grep bloomberg || echo "No bloomberg processes running"

echo "=== Log Files ==="
if [ -f "bot.log" ]; then
    echo "📝 bot.log exists ($(wc -l < bot.log) lines)"
    echo "Last 5 lines:"
    tail -5 bot.log
else
    echo "📝 No bot.log file found"
fi
