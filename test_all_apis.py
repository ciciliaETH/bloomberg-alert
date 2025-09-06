#!/usr/bin/env python3
import sys
import os

# Add current directory to path so we can import from config
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_ai_analysis():
    """Test the AI analysis function directly"""
    print("=== TESTING AI ANALYSIS FUNCTION ===")
    
    # Import our function
    try:
        from bloomberg_simple import generate_ai_analysis, generate_smart_template_analysis
        print("✅ Successfully imported analysis functions")
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        return
    
    # Test headlines
    test_headlines = [
        "Bank Mandiri mencatat laba bersih Rp 15,3 triliun pada semester I-2025",
        "Rupiah menguat 0,5% terhadap dolar AS di tengah optimisme ekonomi",
        "Harga minyak dunia turun 3% akibat kekhawatiran resesi global",
        "BI mempertahankan suku bunga acuan di level 6% untuk stabilitas inflasi"
    ]
    
    for i, headline in enumerate(test_headlines, 1):
        print(f"\n--- Test Case {i} ---")
        print(f"Headline: {headline}")
        
        # Test AI analysis
        print("\n🤖 Testing AI Analysis:")
        result = generate_ai_analysis(headline)
        if result:
            print(f"✅ AI Result ({len(result)} chars):")
            print(result[:200] + "..." if len(result) > 200 else result)
        else:
            print("❌ AI Analysis failed")
        
        # Test smart template
        print("\n📝 Testing Smart Template:")
        template_result = generate_smart_template_analysis(headline)
        if template_result:
            print(f"✅ Template Result ({len(template_result)} chars):")
            print(template_result[:200] + "..." if len(template_result) > 200 else template_result)
        else:
            print("❌ Template failed")

def test_google_api_versions():
    """Test different Google API approaches"""
    print("\n=== TESTING GOOGLE API VERSIONS ===")
    
    try:
        import google.generativeai as genai
        from telegram_config import GEMINI_API_KEY
        
        print(f"✅ google.generativeai imported")
        print(f"✅ API Key configured: {GEMINI_API_KEY[:10]}..." if GEMINI_API_KEY else "❌ No API key")
        
        if not GEMINI_API_KEY:
            return
            
        genai.configure(api_key=GEMINI_API_KEY)
        
        # Test 1: Check available attributes
        print(f"\n📋 Available attributes in genai:")
        attrs = [attr for attr in dir(genai) if not attr.startswith('_')]
        for attr in attrs[:10]:  # Show first 10
            print(f"  - {attr}")
        if len(attrs) > 10:
            print(f"  ... and {len(attrs)-10} more")
        
        # Test 2: Try GenerativeModel
        if hasattr(genai, 'GenerativeModel'):
            print(f"\n✅ GenerativeModel available")
            try:
                model = genai.GenerativeModel('gemini-pro')
                print(f"✅ Model created: {type(model)}")
            except Exception as e:
                print(f"❌ Model creation failed: {e}")
        else:
            print(f"\n❌ GenerativeModel not available")
        
        # Test 3: Try generate_text
        if hasattr(genai, 'generate_text'):
            print(f"\n✅ generate_text available")
            try:
                response = genai.generate_text(prompt="Test prompt")
                print(f"✅ generate_text response: {type(response)}")
            except Exception as e:
                print(f"❌ generate_text failed: {e}")
        else:
            print(f"\n❌ generate_text not available")
        
        # Test 4: Try listing models
        if hasattr(genai, 'list_models'):
            print(f"\n🔄 Trying to list models...")
            try:
                models = genai.list_models()
                print(f"✅ Models listed: {type(models)}")
                if hasattr(models, '__iter__'):
                    model_names = [m.name for m in models][:5]
                    print(f"Available models: {model_names}")
            except Exception as e:
                print(f"❌ list_models failed: {e}")
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")

if __name__ == "__main__":
    print("=== COMPREHENSIVE API TEST ===")
    test_google_api_versions()
    test_ai_analysis()
