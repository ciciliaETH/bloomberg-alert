#!/usr/bin/env python3
# Debug script untuk test AI analysis di VPS dengan berbagai model

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

# Use config key if env key not available
if not env_key and GEMINI_API_KEY:
    env_key = GEMINI_API_KEY

# Test AI analysis with multiple models
if GEMINI_AVAILABLE and env_key:
    try:
        genai.configure(api_key=env_key)
        print("✅ Gemini API key configured")
        
        test_headline = "Fed's Powell Signals Rate Cut Coming Soon"
        
        # List of models to test
        models_to_try = [
            'gemini-1.5-flash',
            'gemini-1.5-pro', 
            'gemini-pro',
            'gemini-1.0-pro'
        ]
        
        success = False
        for model_name in models_to_try:
            try:
                print(f"🔄 Testing model: {model_name}")
                model = genai.GenerativeModel(model_name)
                
                prompt = f"Analyze this headline in one sentence: {test_headline}"
                response = model.generate_content(prompt)
                
                print(f"✅ Model {model_name} SUCCESS!")
                print(f"Response preview: {response.text[:100]}...")
                success = True
                break
                
            except Exception as e:
                print(f"❌ Model {model_name} failed: {e}")
                continue
        
        if not success:
            print("🔄 Trying legacy generate_text API...")
            try:
                response = genai.generate_text(prompt=f"Analyze this headline: {test_headline}")
                result = response.result if hasattr(response, 'result') else str(response)
                print("✅ Legacy API test successful!")
                print(f"Response preview: {result[:100]}...")
            except Exception as e:
                print(f"❌ Legacy API test failed: {e}")
        
    except Exception as e:
        print(f"❌ Gemini API configuration failed: {e}")
else:
    print("❌ Cannot test AI - missing requirements")

print("=== END DEBUG ===")
