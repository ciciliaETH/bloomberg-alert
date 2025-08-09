"""
Script untuk mendapatkan Chat ID dari Telegram Bot
"""

import requests
import json
from telegram_config import TELEGRAM_TOKEN

def get_chat_id_from_updates():
    """Mendapatkan chat ID dari updates terbaru"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data['ok'] and data['result']:
                print("✅ Found updates!")
                
                # Ambil chat ID dari update terbaru
                for update in data['result']:
                    if 'message' in update:
                        chat = update['message']['chat']
                        chat_id = chat['id']
                        user_info = update['message']['from']
                        
                        print(f"\n📱 Chat found:")
                        print(f"   Chat ID: {chat_id}")
                        print(f"   Type: {chat.get('type', 'private')}")
                        print(f"   User: {user_info.get('first_name', '')} {user_info.get('last_name', '')}")
                        if user_info.get('username'):
                            print(f"   Username: @{user_info.get('username')}")
                        
                        return str(chat_id)
                
                print("❌ No chat found in updates")
                return None
            else:
                print("❌ No updates found")
                print("💡 Kirim pesan '/start' ke bot @cicilianews_bot terlebih dahulu")
                return None
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return None

def update_config_with_chat_id(chat_id):
    """Update telegram_config.py dengan chat ID yang benar"""
    try:
        config_content = f'''# Konfigurasi Telegram Bot
# Bot Token dari @BotFather

TELEGRAM_TOKEN = "{TELEGRAM_TOKEN}"

# Chat ID yang di-detect otomatis
TELEGRAM_CHAT_ID = "{chat_id}"

# Contoh format pesan yang akan dikirim:
# 🔔 Bloomberg Alert
# 
# 📅 Waktu: Sat, 9 Aug 2025 05:03:05 -0000
# 
# 📰 Headline:
# The Bank of England Has Rarely Been This Split Over Inflation
'''
        
        with open('telegram_config.py', 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        print(f"✅ telegram_config.py updated with Chat ID: {chat_id}")
        return True
        
    except Exception as e:
        print(f"❌ Error updating config: {e}")
        return False

def test_send_message(chat_id):
    """Test kirim pesan ke chat ID yang ditemukan"""
    try:
        message = "🎉 *Bloomberg Bot Setup Complete!*\n\nBot siap memonitor email Bloomberg.\n\nKirim `/start` untuk mulai monitoring."
        
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        
        response = requests.post(url, data=payload, timeout=10)
        
        if response.status_code == 200:
            print("✅ Test message sent successfully!")
            return True
        else:
            print(f"❌ Failed to send test message: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending test message: {e}")
        return False

def main():
    print("🔍 CHAT ID DETECTOR")
    print("=" * 50)
    print()
    print("Pastikan sudah kirim pesan ke bot @cicilianews_bot")
    print("Kemudian tekan Enter untuk detect chat ID...")
    input()
    
    print("🔍 Looking for chat ID...")
    chat_id = get_chat_id_from_updates()
    
    if chat_id:
        print(f"\n🎯 Chat ID found: {chat_id}")
        
        if update_config_with_chat_id(chat_id):
            print("\n🧪 Testing message send...")
            if test_send_message(chat_id):
                print("\n🎉 Setup complete!")
                print("🚀 Sekarang jalankan: python bloomberg_simple.py")
            else:
                print("\n⚠️ Config updated but test message failed")
        else:
            print("\n❌ Failed to update config")
    else:
        print("\n❌ Chat ID not found")
        print("💡 Steps to fix:")
        print("1. Buka Telegram")
        print("2. Cari @cicilianews_bot") 
        print("3. Kirim pesan '/start'")
        print("4. Jalankan script ini lagi")

if __name__ == '__main__':
    main()
