#!/bin/bash

echo "=== Bloomberg Bot Setup & Test ==="

# Pull latest changes
git pull

# Install dependencies (if needed)
pip install -r requirements.txt

echo "=== Testing Smart Template Analysis ==="
python test_all_apis.py

echo "=== Testing Bot with New Analysis ==="
python -c "
from bloomberg_simple import generate_smart_template_analysis
result = generate_smart_template_analysis('Bank Mandiri mencatat laba bersih Rp 15,3 triliun')
print('📊 SAMPLE ANALYSIS:')
print(result)
print('\n✅ Smart template working!')
"

echo "=== Starting Bot ==="
nohup python bloomberg_simple.py > bot.log 2>&1 &
echo "Bot started! Check bot.log for logs"

echo "=== Setup Complete ==="
echo "✅ Smart template analysis implemented"
echo "✅ Bot will work even if AI fails" 
echo "✅ Analysis quality improved with keyword detection"
echo "📝 Check bot.log for real-time logs"
