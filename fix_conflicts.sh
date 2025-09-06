#!/bin/bash

echo "=== Resolving Git Conflicts ==="

# Stash local changes
echo "📦 Stashing local changes..."
git stash

# Pull latest updates
echo "⬇️ Pulling latest updates..."
git pull

# Show what was stashed (optional)
echo "📋 Stashed changes:"
git stash list

echo "=== Installing Dependencies ==="
pip install google-generativeai==0.1.0rc1

echo "=== Testing Smart Template Analysis ==="
python test_all_apis.py

echo "=== Testing Bot ==="
echo "Testing smart template..."
python -c "
try:
    from bloomberg_simple import generate_smart_template_analysis
    result = generate_smart_template_analysis('Bank Mandiri mencatat laba bersih Rp 15,3 triliun pada semester I-2025')
    print('✅ SMART TEMPLATE TEST:')
    print(result)
    print('\n✅ Template analysis working!')
except Exception as e:
    print(f'❌ Template test failed: {e}')
"

echo "=== Starting Bot ==="
# Kill existing bot process if running
pkill -f bloomberg_simple.py 2>/dev/null || echo "No existing bot process"

# Start new bot instance
nohup python bloomberg_simple.py > bot.log 2>&1 &
echo "✅ Bot started! PID: $!"

echo "=== Status Check ==="
sleep 3
if pgrep -f bloomberg_simple.py > /dev/null; then
    echo "✅ Bot is running successfully"
    echo "📝 Check logs: tail -f bot.log"
else
    echo "❌ Bot failed to start"
    echo "📝 Check errors: cat bot.log"
fi

echo "=== Setup Complete ==="
echo "Commands to monitor:"
echo "  tail -f bot.log      # View live logs"
echo "  ps aux | grep bloomberg  # Check if running"
echo "  pkill -f bloomberg_simple.py  # Stop bot"
