"""
Helper script untuk setup Telegram Bot
"""

import requests
import json

def get_chat_id(bot_token):
    """Mendapatkan chat ID dari bot Telegram"""
    try:
        url = f"https://api.telegram.org/bot{bot_token}/getUpdates"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            
            if data['ok'] and data['result']:
                print("✅ Data ditemukan:")
                print(json.dumps(data, indent=2))
                
                # Ekstrak chat IDs
                chat_ids = set()
                for update in data['result']:
                    if 'message' in update and 'chat' in update['message']:
                        chat_id = update['message']['chat']['id']
                        chat_ids.add(chat_id)
                        
                        # Tampilkan info chat
                        chat = update['message']['chat']
                        print(f"\n📱 Chat ditemukan:")
                        print(f"   Chat ID: {chat_id}")
                        print(f"   Type: {chat.get('type', 'unknown')}")
                        if chat.get('first_name'):
                            print(f"   Name: {chat.get('first_name')} {chat.get('last_name', '')}")
                        if chat.get('username'):
                            print(f"   Username: @{chat.get('username')}")
                
                if chat_ids:
                    print(f"\n🎯 Chat IDs yang ditemukan: {list(chat_ids)}")
                    return list(chat_ids)
                else:
                    print("\n❌ Tidak ada chat ID ditemukan.")
                    print("💡 Kirim pesan ke bot terlebih dahulu, lalu jalankan script ini lagi.")
                    return []
            else:
                print("❌ Tidak ada update ditemukan.")
                print("💡 Kirim pesan ke bot terlebih dahulu.")
                return []
        else:
            print(f"❌ Error: {response.status_code} - {response.text}")
            return []
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return []

def test_send_message(bot_token, chat_id):
    """Test mengirim pesan ke Telegram"""
    try:
        message = "🔔 Test pesan dari Bloomberg Bot!\n\nBot berhasil terhubung! ✅"
        
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        payload = {
            'chat_id': chat_id,
            'text': message,
            'parse_mode': 'Markdown'
        }
        
        response = requests.post(url, data=payload, timeout=10)
        
        if response.status_code == 200:
            print("✅ Pesan test berhasil dikirim!")
            return True
        else:
            print(f"❌ Gagal mengirim pesan: {response.status_code} - {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error mengirim pesan: {e}")
        return False

def update_config_file(bot_token, chat_id):
    """Update file telegram_config.py dengan token dan chat ID yang benar"""
    try:
        config_content = f'''# Konfigurasi Telegram Bot
# File ini di-generate otomatis oleh telegram_setup.py

# Bot Token dari @BotFather
TELEGRAM_TOKEN = "{bot_token}"

# Chat ID dari conversation dengan bot
TELEGRAM_CHAT_ID = "{chat_id}"

# Format pesan yang akan dikirim:
# 🔔 Bloomberg Alert
# 
# 📅 Waktu: Sat, 9 Aug 2025 05:03:05 -0000
# 
# 📰 Headline:
# The Bank of England Has Rarely Been This Split Over Inflation
'''
        
        with open('telegram_config.py', 'w', encoding='utf-8') as f:
            f.write(config_content)
        
        print("✅ File telegram_config.py berhasil diupdate!")
        return True
        
    except Exception as e:
        print(f"❌ Error update config: {e}")
        return False

def main():
    print("🤖 TELEGRAM BOT SETUP HELPER")
    print("=" * 50)
    print()
    print("Langkah setup:")
    print("1. Buat bot baru dengan @BotFather di Telegram")
    print("2. Dapatkan token dari @BotFather") 
    print("3. Kirim pesan ke bot yang baru dibuat")
    print("4. Jalankan script ini untuk mendapatkan chat ID")
    print()
    
    while True:
        bot_token = input("🔑 Masukkan Bot Token: ").strip()
        
        if not bot_token or bot_token == '8122220616:AAFI8xFd2O0X1UiJWBWvO8j5-pgeysLCbpc':
            print("❌ Token tidak valid!")
            continue
        
        if not bot_token.count(':') == 1:
            print("❌ Format token salah! Contoh: 123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi")
            continue
        
        break
    
    print(f"\n🔍 Mencari chat IDs untuk bot: {bot_token[:10]}...")
    chat_ids = get_chat_id(bot_token)
    
    if not chat_ids:
        print("\n💡 Tips:")
        print("- Pastikan sudah kirim pesan ke bot")
        print("- Bot token harus benar")
        print("- Coba kirim pesan lagi lalu jalankan script ini")
        return
    
    if len(chat_ids) == 1:
        chat_id = chat_ids[0]
        print(f"\n✅ Menggunakan Chat ID: {chat_id}")
    else:
        print(f"\n📱 Pilih Chat ID:")
        for i, cid in enumerate(chat_ids, 1):
            print(f"   {i}. {cid}")
        
        while True:
            try:
                choice = int(input("\nPilih nomor: ")) - 1
                if 0 <= choice < len(chat_ids):
                    chat_id = chat_ids[choice]
                    break
                else:
                    print("❌ Pilihan tidak valid!")
            except ValueError:
                print("❌ Masukkan angka yang valid!")
    
    print(f"\n🧪 Testing dengan Chat ID: {chat_id}")
    if test_send_message(bot_token, chat_id):
        print("\n💾 Menyimpan konfigurasi...")
        if update_config_file(bot_token, chat_id):
            print("\n🎉 Setup selesai!")
            print("🚀 Sekarang jalankan: python bloomberg_simple.py")
        else:
            print("\n❌ Gagal menyimpan konfigurasi")
    else:
        print("\n❌ Test gagal. Periksa token dan chat ID.")

if __name__ == '__main__':
    main()
