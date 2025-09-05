#!/usr/bin/env python3
# Debug script untuk test AI analysis di VPS

import sys
import os

print("=== DEBUG AI ANALYSIS ===")
print(f"Python version: {sys.version}")
print(f"Working directory: {os.getcwd()}")

# Test import Gemini
try:
    import google.generativeai as genai
    print("✅ google.generativeai imported successfully")
    GEMINI_AVAILABLE = True
except ImportError as e:
    print(f"❌ Failed to import google.generativeai: {e}")
    GEMINI_AVAILABLE = False

# Test config loading
try:
    from telegram_config import GEMINI_API_KEY
    print(f"✅ GEMINI_API_KEY from config: {GEMINI_API_KEY[:10]}..." if GEMINI_API_KEY else "❌ GEMINI_API_KEY is None")
except ImportError:
    print("❌ Failed to import from telegram_config")
    GEMINI_API_KEY = None

# Test environment variables
env_key = os.getenv('GEMINI_API_KEY')
print(f"Environment GEMINI_API_KEY: {env_key[:10]}..." if env_key else "❌ No GEMINI_API_KEY in environment")

# Test AI analysis
if GEMINI_AVAILABLE and GEMINI_API_KEY:
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        test_headline = "Fed's Powell Signals Rate Cut Coming Soon"
        prompt = f"Analyze this headline: {test_headline}"
        
        print("🔄 Testing Gemini API...")
        response = model.generate_content(prompt)
        print("✅ Gemini API test successful!")
        print(f"Response preview: {response.text[:100]}...")
        
    except Exception as e:
        print(f"❌ Gemini API test failed: {e}")
else:
    print("❌ Cannot test AI - missing requirements")

print("=== END DEBUG ===")
