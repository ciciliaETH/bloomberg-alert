#!/usr/bin/env python3
"""
Fix AI analysis for old google-generativeai version
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_available_models():
    """Test which models are actually available"""
    print("=== TESTING AVAILABLE MODELS ===")
    
    try:
        import google.generativeai as genai
        from telegram_config import GEMINI_API_KEY
        
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Method 1: Try to list models
        try:
            print("🔄 Trying to list available models...")
            if hasattr(genai, 'list_models'):
                models = genai.list_models()
                print("✅ Available models:")
                for model in models:
                    print(f"  - {model.name}")
            else:
                print("❌ list_models not available")
        except Exception as e:
            print(f"❌ list_models failed: {e}")
        
        # Method 2: Test different model names for generate_text
        old_models = [
            'models/text-bison-001',
            'text-bison-001', 
            'models/chat-bison-001',
            'chat-bison-001',
            'text-bison',
            'chat-bison'
        ]
        
        test_prompt = "Analisis: Bank Mandiri laba naik"
        
        for model_name in old_models:
            try:
                print(f"🔄 Testing model: {model_name}")
                response = genai.generate_text(
                    model=model_name,
                    prompt=test_prompt,
                    temperature=0.7,
                    max_output_tokens=100
                )
                
                if response and hasattr(response, 'result') and response.result:
                    print(f"✅ SUCCESS with {model_name}: {response.result[:50]}...")
                    return model_name
                elif response and hasattr(response, 'candidates'):
                    print(f"✅ SUCCESS with {model_name}: candidates found")
                    return model_name
                else:
                    print(f"❌ {model_name}: No result")
                    
            except Exception as e:
                print(f"❌ {model_name} failed: {e}")
        
        # Method 3: Test direct API with different endpoints
        import requests
        
        endpoints = [
            "https://generativelanguage.googleapis.com/v1beta/models/text-bison-001:generateText",
            "https://generativelanguage.googleapis.com/v1/models/text-bison-001:generateText",
            "https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText"
        ]
        
        for endpoint in endpoints:
            try:
                print(f"🔄 Testing endpoint: {endpoint}")
                
                payload = {
                    "prompt": {"text": test_prompt},
                    "temperature": 0.7,
                    "candidateCount": 1
                }
                
                response = requests.post(
                    f"{endpoint}?key={GEMINI_API_KEY}",
                    json=payload,
                    timeout=30
                )
                
                print(f"Status: {response.status_code}")
                if response.status_code == 200:
                    result = response.json()
                    print(f"✅ SUCCESS: {str(result)[:100]}...")
                    return endpoint
                else:
                    print(f"❌ Error: {response.text[:100]}")
                    
            except Exception as e:
                print(f"❌ Endpoint {endpoint} failed: {e}")
        
        print("❌ No working models or endpoints found")
        return None
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return None

if __name__ == "__main__":
    working_model = test_available_models()
    
    if working_model:
        print(f"\n✅ WORKING MODEL/ENDPOINT FOUND: {working_model}")
        print("Use this in the AI function!")
    else:
        print(f"\n❌ NO WORKING MODEL FOUND")
        print("The google-generativeai version might be too old")
        print("Try upgrading: pip install google-generativeai --upgrade")
