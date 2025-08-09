"""
Check dependencies untuk Bloomberg Telegram Bot
"""

import sys

def check_imports():
    """Check semua import yang diperlukan"""
    required_modules = [
        'google.auth.transport.requests',
        'google.oauth2.credentials', 
        'google_auth_oauthlib.flow',
        'googleapiclient.discovery',
        'googleapiclient.errors',
        'requests'
    ]
    
    print("🔍 CHECKING DEPENDENCIES")
    print("="*50)
    
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module}")
            missing_modules.append(module)
    
    print()
    
    if missing_modules:
        print("❌ MISSING DEPENDENCIES:")
        print("Run the following commands:")
        print()
        if any('google' in m for m in missing_modules):
            print("pip install google-auth google-auth-oauthlib google-auth-httplib2 google-api-python-client")
        if 'requests' in missing_modules:
            print("pip install requests")
        print()
        return False
    else:
        print("✅ ALL DEPENDENCIES OK!")
        return True

def check_config_files():
    """Check apakah file konfigurasi ada"""
    import os
    
    print("📁 CHECKING CONFIG FILES")
    print("="*50)
    
    files = {
        'credentials.json': 'Google OAuth credentials',
        'telegram_config.py': 'Telegram bot configuration'
    }
    
    all_good = True
    
    for filename, description in files.items():
        if os.path.exists(filename):
            print(f"✅ {filename} - {description}")
        else:
            print(f"❌ {filename} - {description}")
            all_good = False
    
    print()
    
    if not all_good:
        print("❌ MISSING CONFIG FILES:")
        if not os.path.exists('credentials.json'):
            print("• Download credentials.json from Google Cloud Console")
        if not os.path.exists('telegram_config.py'):
            print("• Run: python telegram_setup.py")
        print()
        return False
    else:
        print("✅ ALL CONFIG FILES OK!")
        return True

def main():
    print("🔧 BLOOMBERG TELEGRAM BOT - DEPENDENCY CHECK")
    print("="*60)
    print()
    
    deps_ok = check_imports()
    print()
    config_ok = check_config_files()
    print()
    
    if deps_ok and config_ok:
        print("🎉 READY TO RUN!")
        print("🚀 Execute: python bloomberg_simple.py")
        print("📱 Then send /start to your Telegram bot")
    else:
        print("❌ NOT READY")
        print("💡 Fix the issues above first")
    
    print()
    print("📋 QUICK SETUP CHECKLIST:")
    print("1. ✅ Install dependencies: pip install -r requirements.txt")
    print("2. ✅ Setup Google OAuth: credentials.json")
    print("3. ✅ Setup Telegram bot: python telegram_setup.py") 
    print("4. ✅ Run bot: python bloomberg_simple.py")
    print("5. ✅ Send /start command to bot")

if __name__ == '__main__':
    main()
