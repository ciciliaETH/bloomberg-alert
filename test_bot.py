"""
Test bot Telegram - untuk verify token dan chat ID
"""

import requests
import json

def test_bot_token(token):
    """Test apakah bot token valid"""
    try:
        url = f"https://api.telegram.org/bot{token}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok'):
                bot_info = data['result']
                print("✅ Bot Token Valid!")
                print(f"🤖 Bot Name: {bot_info.get('first_name')}")
                print(f"👤 Username: @{bot_info.get('username')}")
                print(f"🆔 Bot ID: {bot_info.get('id')}")
                return True
            else:
                print("❌ Bot Token Invalid!")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing token: {e}")
        return False

def get_updates(token):
    """Mendapatkan updates terbaru dari bot"""
    try:
        url = f"https://api.telegram.org/bot{token}/getUpdates"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get('ok') and data.get('result'):
                print("📬 Recent Messages:")
                for update in data['result'][-5:]:  # Show last 5 updates
                    if 'message' in update:
                        msg = update['message']
                        chat = msg['chat']
                        user = msg.get('from', {})
                        
                        print(f"  💬 Chat ID: {chat['id']}")
                        print(f"     Type: {chat['type']}")
                        print(f"     User: {user.get('first_name', 'Unknown')}")
                        print(f"     Text: {msg.get('text', 'No text')[:50]}")
                        print(f"     Date: {msg.get('date')}")
                        print()
                
                # Extract unique chat IDs
                chat_ids = set()
                for update in data['result']:
                    if 'message' in update:
                        chat_ids.add(update['message']['chat']['id'])
                
                if chat_ids:
                    print(f"🎯 Available Chat IDs: {list(chat_ids)}")
                    return list(chat_ids)
                else:
                    print("❌ No chat IDs found")
                    return []
            else:
                print("❌ No updates found")
                print("💡 Kirim pesan ke bot terlebih dahulu")
                return []
        else:
            print(f"❌ Error getting updates: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"❌ Error getting updates: {e}")
        return []

def send_test_message(token, chat_id):
    """Kirim pesan test"""
    try:
        url = f"https://api.telegram.org/bot{token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': '🧪 Test message from Bloomberg Bot!\n\nBot is working correctly! ✅',
            'parse_mode': 'Markdown'
        }
        
        response = requests.post(url, data=payload, timeout=10)
        
        if response.status_code == 200:
            print("✅ Test message sent successfully!")
            return True
        else:
            print(f"❌ Failed to send message: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return False

def main():
    print("🧪 TELEGRAM BOT TESTER")
    print("=" * 50)
    
    # Try to load from config first
    try:
        from telegram_config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
        print(f"📄 Config loaded:")
        print(f"   Token: {TELEGRAM_TOKEN[:20]}...")
        print(f"   Chat ID: {TELEGRAM_CHAT_ID}")
        token = TELEGRAM_TOKEN
        chat_id = TELEGRAM_CHAT_ID if TELEGRAM_CHAT_ID != 'YOUR_CHAT_ID' else None
    except ImportError:
        print("❌ No telegram_config.py found")
        token = input("🔑 Enter Bot Token: ").strip()
        chat_id = None
    
    print(f"\n🔍 Testing bot token...")
    if not test_bot_token(token):
        print("❌ Bot token is invalid!")
        return
    
    print(f"\n📬 Getting recent updates...")
    available_chat_ids = get_updates(token)
    
    if not chat_id and available_chat_ids:
        if len(available_chat_ids) == 1:
            chat_id = available_chat_ids[0]
            print(f"✅ Using chat ID: {chat_id}")
        else:
            print("🎯 Multiple chat IDs found. Choose one:")
            for i, cid in enumerate(available_chat_ids, 1):
                print(f"   {i}. {cid}")
            
            try:
                choice = int(input("Select number: ")) - 1
                chat_id = available_chat_ids[choice]
            except (ValueError, IndexError):
                print("❌ Invalid choice")
                return
    
    if chat_id:
        print(f"\n🧪 Sending test message to {chat_id}...")
        if send_test_message(token, chat_id):
            # Update config file
            try:
                config_content = f'''# Auto-generated Telegram config
TELEGRAM_TOKEN = "{token}"
TELEGRAM_CHAT_ID = "{chat_id}"
'''
                with open('telegram_config.py', 'w') as f:
                    f.write(config_content)
                print("✅ Config file updated!")
                print("🚀 Now you can run: python bloomberg_simple.py")
            except Exception as e:
                print(f"⚠️ Could not update config: {e}")
        else:
            print("❌ Test message failed")
    else:
        print("❌ No chat ID available")
        print("💡 Send a message to your bot first, then run this script again")

if __name__ == '__main__':
    main()
