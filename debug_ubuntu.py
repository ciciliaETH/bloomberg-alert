#!/usr/bin/env python3
"""
Debug script for AI analysis on Ubuntu 20.04
Tests all possible AI methods and configurations
"""

import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_system_info():
    """Test system information"""
    print("=== SYSTEM INFO ===")
    print(f"Python version: {sys.version}")
    print(f"Platform: {sys.platform}")
    print(f"Working directory: {os.getcwd()}")
    
    # Check virtual environment
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("✅ Running in virtual environment")
    else:
        print("⚠️ Not in virtual environment")

def test_imports():
    """Test all required imports"""
    print("\n=== TESTING IMPORTS ===")
    
    # Test requests
    try:
        import requests
        print(f"✅ requests: {requests.__version__}")
    except ImportError as e:
        print(f"❌ requests failed: {e}")
    
    # Test Google Generative AI
    try:
        import google.generativeai as genai
        print(f"✅ google.generativeai imported")
        
        # Check available attributes
        attrs = [attr for attr in dir(genai) if not attr.startswith('_')]
        print(f"Available methods: {', '.join(attrs[:5])}...")
        
        if hasattr(genai, 'GenerativeModel'):
            print("✅ GenerativeModel available")
        else:
            print("❌ GenerativeModel NOT available")
            
        if hasattr(genai, 'generate_text'):
            print("✅ generate_text available")
        else:
            print("❌ generate_text NOT available")
            
    except ImportError as e:
        print(f"❌ google.generativeai failed: {e}")
        return False
    
    return True

def test_api_key():
    """Test API key configuration"""
    print("\n=== TESTING API KEY ===")
    
    try:
        from telegram_config import GEMINI_API_KEY
        if GEMINI_API_KEY and GEMINI_API_KEY != 'YOUR_GEMINI_KEY':
            print(f"✅ API key loaded: {GEMINI_API_KEY[:10]}...")
            return GEMINI_API_KEY
        else:
            print("❌ No valid API key found")
            return None
    except ImportError:
        print("❌ telegram_config.py not found")
        return None

def test_ai_methods(api_key):
    """Test different AI generation methods"""
    if not api_key:
        print("❌ Cannot test AI without API key")
        return
    
    print("\n=== TESTING AI METHODS ===")
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        test_prompt = "Analisis singkat: Bank Mandiri mencatat laba bersih Rp 15 triliun"
        
        # Test Method 1: GenerativeModel with gemini-1.5-flash
        try:
            print("🔄 Testing GenerativeModel + gemini-1.5-flash...")
            model = genai.GenerativeModel('gemini-1.5-flash')
            response = model.generate_content(test_prompt)
            if response and hasattr(response, 'text'):
                result = response.text.strip()
                print(f"✅ SUCCESS: {result[:100]}...")
                return True
        except Exception as e:
            print(f"❌ Method 1 failed: {e}")
        
        # Test Method 2: GenerativeModel with gemini-pro
        try:
            print("🔄 Testing GenerativeModel + gemini-pro...")
            model = genai.GenerativeModel('gemini-pro')
            response = model.generate_content(test_prompt)
            if response and hasattr(response, 'text'):
                result = response.text.strip()
                print(f"✅ SUCCESS: {result[:100]}...")
                return True
        except Exception as e:
            print(f"❌ Method 2 failed: {e}")
        
        # Test Method 3: generate_text
        try:
            print("🔄 Testing generate_text...")
            response = genai.generate_text(
                model='models/text-bison-001',
                prompt=test_prompt,
                temperature=0.7
            )
            if response and hasattr(response, 'result'):
                result = response.result.strip()
                print(f"✅ SUCCESS: {result[:100]}...")
                return True
        except Exception as e:
            print(f"❌ Method 3 failed: {e}")
        
        # Test Method 4: Direct REST API
        try:
            print("🔄 Testing direct REST API...")
            import requests
            
            url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
            
            payload = {
                "contents": [{
                    "parts": [{"text": test_prompt}]
                }]
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            print(f"Status: {response.status_code}")
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and result['candidates']:
                    content = result['candidates'][0].get('content', {})
                    if 'parts' in content and content['parts']:
                        text = content['parts'][0].get('text', '')
                        if text:
                            print(f"✅ SUCCESS: {text[:100]}...")
                            return True
            else:
                print(f"❌ API Error: {response.text[:200]}...")
                
        except Exception as e:
            print(f"❌ Method 4 failed: {e}")
        
        print("❌ All AI methods failed")
        return False
        
    except Exception as e:
        print(f"❌ AI testing failed: {e}")
        return False

def test_full_analysis():
    """Test the full analysis function"""
    print("\n=== TESTING FULL ANALYSIS ===")
    
    try:
        from bloomberg_simple import generate_ai_analysis
        
        test_headlines = [
            "Bank Mandiri mencatat laba bersih Rp 15,3 triliun pada semester I-2025",
            "Rupiah menguat 0,5% terhadap dolar AS"
        ]
        
        for headline in test_headlines:
            print(f"\n📰 Testing: {headline}")
            result = generate_ai_analysis(headline)
            
            if result:
                print(f"✅ Analysis generated ({len(result)} chars)")
                print(f"Preview: {result[:150]}...")
            else:
                print("❌ Analysis failed")
                
    except ImportError as e:
        print(f"❌ Cannot import bloomberg_simple: {e}")
    except Exception as e:
        print(f"❌ Full analysis test failed: {e}")

if __name__ == "__main__":
    print("🔧 AI DEBUG TOOL FOR UBUNTU 20.04")
    print("=" * 50)
    
    test_system_info()
    
    if test_imports():
        api_key = test_api_key()
        if api_key:
            if test_ai_methods(api_key):
                test_full_analysis()
            else:
                print("\n❌ AI methods failed - check API key or network")
        else:
            print("\n❌ No API key - cannot test AI")
    else:
        print("\n❌ Import failed - install dependencies first")
    
    print("\n" + "=" * 50)
    print("🏁 Debug complete!")
