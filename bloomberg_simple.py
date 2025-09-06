import os.path
import json
import requests
import time
import threading
from datetime import datetime, timedelta
import email.utils
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Try to import AI libraries (optional)
try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False
    print("⚠️ Google Generative AI not installed, AI analysis will be disabled")

# Import konfigurasi Telegram
try:
    # Try environment variables first (for production)
    import os
    TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID', '')
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    if not TELEGRAM_TOKEN:
        # Fallback to local config file
        from telegram_config import TELEGRAM_TOKEN, TELEGRAM_CHAT_ID
        try:
            from telegram_config import GEMINI_API_KEY
        except ImportError:
            GEMINI_API_KEY = None
        
    print(f"✅ Loaded config - Token: {TELEGRAM_TOKEN[:10]}..., Chat ID: {TELEGRAM_CHAT_ID}")
except ImportError:
    # Fallback jika file config tidak ada
    TELEGRAM_TOKEN = 'YOUR_BOT_TOKEN'
    TELEGRAM_CHAT_ID = 'YOUR_CHAT_ID'
    GEMINI_API_KEY = 'YOUR_GEMINI_KEY'
    print("❌ File telegram_config.py tidak ditemukan!")
    print("🔧 Jalankan: python telegram_setup.py untuk setup bot")
    exit(1)

# Setup Gemini AI
if GEMINI_AVAILABLE and GEMINI_API_KEY and GEMINI_API_KEY != 'YOUR_GEMINI_KEY':
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        print("🤖 Gemini AI Analysis enabled (FREE)")
    except Exception as e:
        print(f"⚠️ Gemini setup error: {e}")
else:
    print("⚠️ Gemini not available, AI analysis disabled")

# SCOPES yang diperlukan untuk mengakses Gmail
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# File untuk menyimpan ID email terakhir yang diproses
LAST_PROCESSED_ID_FILE = 'last_email_id.txt'
LAST_EMAIL_DATA_FILE = 'last_email_data.json'
STATUS_FILE = 'monitoring_status.json'
SUBSCRIBERS_FILE = 'subscribers.json'

# Global status monitoring
monitoring_active = False
last_update_offset = 0
subscribers = set()  # Set of chat IDs yang subscribe

def load_subscribers():
    """Load list subscribers dari file"""
    global subscribers
    if os.path.exists(SUBSCRIBERS_FILE):
        try:
            with open(SUBSCRIBERS_FILE, 'r') as f:
                data = json.load(f)
                subscribers = set(str(chat_id) for chat_id in data.get('subscribers', []))
                print(f"📱 Loaded {len(subscribers)} subscribers")
        except:
            subscribers = set()
    else:
        subscribers = set()

def save_subscribers():
    """Simpan list subscribers ke file"""
    try:
        data = {
            'subscribers': list(subscribers),
            'updated': time.time()
        }
        with open(SUBSCRIBERS_FILE, 'w') as f:
            json.dump(data, f)
        print(f"💾 Saved {len(subscribers)} subscribers")
    except Exception as e:
        print(f"❌ Error saving subscribers: {e}")

def add_subscriber(chat_id):
    """Tambahkan subscriber baru"""
    global subscribers
    chat_id = str(chat_id)
    if chat_id not in subscribers:
        subscribers.add(chat_id)
        save_subscribers()
        print(f"➕ Added new subscriber: {chat_id}")
        return True
    return False

def remove_subscriber(chat_id):
    """Hapus subscriber"""
    global subscribers
    chat_id = str(chat_id)
    if chat_id in subscribers:
        subscribers.remove(chat_id)
        save_subscribers()
        print(f"➖ Removed subscriber: {chat_id}")
        return True
    return False

def get_monitoring_status():
    """Membaca status monitoring dari file"""
    if os.path.exists(STATUS_FILE):
        try:
            with open(STATUS_FILE, 'r') as f:
                status = json.load(f)
                return status.get('active', False)
        except:
            return False
    return False

def save_monitoring_status(active):
    """Menyimpan status monitoring ke file"""
    status = {'active': active, 'timestamp': time.time()}
    with open(STATUS_FILE, 'w') as f:
        json.dump(status, f)

def get_telegram_updates(offset=0):
    """Mendapatkan update terbaru dari Telegram"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/getUpdates"
        params = {
            'offset': offset,
            'timeout': 10,
            'allowed_updates': ['message']  
        }
        response = requests.get(url, params=params, timeout=15)
        
        if response.status_code == 200:
            return response.json()
        elif response.status_code == 409:
            print("⚠️ Conflict detected (409) - clearing webhook...")
            clear_webhook()
            time.sleep(2)
            return None
        else:
            print(f"❌ Error getting updates: {response.status_code}")
            return None
    except Exception as e:
        print(f"❌ Error getting updates: {e}")
        return None

def clear_webhook():
    """Menghapus webhook yang mungkin aktif"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/deleteWebhook"
        response = requests.post(url, timeout=10)
        if response.status_code == 200:
            print("✅ Webhook cleared successfully")
        return response.json()
    except Exception as e:
        print(f"❌ Error clearing webhook: {e}")
        return None

def send_telegram_message(text, chat_id=None, reply_to_message_id=None, parse_mode='HTML'):
    """Mengirim pesan ke Telegram (single chat)"""
    try:
        # Gunakan chat_id yang diberikan, atau default TELEGRAM_CHAT_ID
        target_chat_id = chat_id if chat_id else TELEGRAM_CHAT_ID
        
        # Skip jika chat_id kosong
        if not target_chat_id:
            print("⚠️ Chat ID empty, skipping message")
            return False
        
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            'chat_id': target_chat_id,
            'text': text
        }
        
        # Add parse_mode if specified
        if parse_mode:
            payload['parse_mode'] = parse_mode
        
        if reply_to_message_id:
            payload['reply_to_message_id'] = reply_to_message_id
        
        response = requests.post(url, data=payload, timeout=10)
        
        if response.status_code == 200:
            return True
        else:
            print(f"❌ Error sending message to {target_chat_id}: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending message: {e}")
        return False

def send_telegram_message_with_keyboard(text, chat_id=None, keyboard=None, parse_mode='HTML'):
    """Mengirim pesan ke Telegram dengan inline keyboard"""
    try:
        # Gunakan chat_id yang diberikan, atau default TELEGRAM_CHAT_ID
        target_chat_id = chat_id if chat_id else TELEGRAM_CHAT_ID
        
        # Skip jika chat_id kosong
        if not target_chat_id:
            print("⚠️ Chat ID empty, skipping message")
            return False
        
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
        payload = {
            'chat_id': target_chat_id,
            'text': text
        }
        
        # Add parse_mode if specified
        if parse_mode:
            payload['parse_mode'] = parse_mode
        
        if keyboard:
            import json
            payload['reply_markup'] = json.dumps(keyboard)
        
        response = requests.post(url, data=payload, timeout=10)
        
        if response.status_code == 200:
            return True
        else:
            print(f"❌ Error sending message with keyboard to {target_chat_id}: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error sending message with keyboard: {e}")
        return False

def broadcast_to_subscribers(text):
    """Broadcast pesan ke semua subscribers"""
    if not subscribers:
        print("❌ No subscribers to broadcast to")
        return False
    
    success_count = 0
    failed_count = 0
    
    for chat_id in subscribers.copy():  # Use copy to avoid modification during iteration
        if send_telegram_message(text, chat_id):
            success_count += 1
        else:
            failed_count += 1
            # Optionally remove failed chat_ids (user might have blocked bot)
    
    print(f"📤 Broadcast sent: {success_count} success, {failed_count} failed")
    return success_count > 0

def broadcast_to_subscribers_with_ai(text, headline, ai_analysis):
    """Broadcast pesan ke semua subscribers dengan inline keyboard untuk AI analysis"""
    if not subscribers:
        print("❌ No subscribers to broadcast to")
        return False
    
    success_count = 0
    failed_count = 0
    
    # Create inline keyboard untuk show AI analysis
    keyboard = {
        "inline_keyboard": [[
            {
                "text": "📖 Show AI Analysis", 
                "callback_data": f"show_ai:{len(headline)}"  # Use headline length as unique ID
            }
        ]]
    }
    
    # Store AI analysis temporarily (simple in-memory storage)
    if not hasattr(broadcast_to_subscribers_with_ai, 'ai_cache'):
        broadcast_to_subscribers_with_ai.ai_cache = {}
    
    broadcast_to_subscribers_with_ai.ai_cache[str(len(headline))] = {
        'headline': headline,
        'analysis': ai_analysis or "AI analysis not available"
    }
    
    for chat_id in subscribers.copy():
        if send_telegram_message_with_keyboard(text, chat_id, keyboard):
            success_count += 1
        else:
            failed_count += 1
    
    print(f"📤 Broadcast with AI button sent: {success_count} success, {failed_count} failed")
    return success_count > 0

def auto_detect_chat_id():
    """Auto-detect chat ID dari pesan yang masuk"""
    global TELEGRAM_CHAT_ID
    
    try:
        updates = get_telegram_updates()
        if updates and updates.get('ok') and updates.get('result'):
            for update in updates['result']:
                if 'message' in update:
                    chat_id = str(update['message']['chat']['id'])
                    if TELEGRAM_CHAT_ID == 'YOUR_CHAT_ID':
                        print(f"🔍 Auto-detected Chat ID: {chat_id}")
                        TELEGRAM_CHAT_ID = chat_id
                        
                        # Update config file
                        try:
                            config_content = f'''# Auto-generated Telegram config
TELEGRAM_TOKEN = "{TELEGRAM_TOKEN}"
TELEGRAM_CHAT_ID = "{TELEGRAM_CHAT_ID}"
'''
                            with open('telegram_config.py', 'w') as f:
                                f.write(config_content)
                            print("✅ Config updated with detected chat ID")
                        except:
                            print("⚠️ Could not update config file")
                        
                        return chat_id
            return TELEGRAM_CHAT_ID
    except Exception as e:
        print(f"❌ Error auto-detecting chat ID: {e}")
        return TELEGRAM_CHAT_ID

def handle_telegram_command(message):
    """Handle commands dari Telegram dengan auto-subscribe"""
    global monitoring_active
    
    text = message.get('text', '').strip()
    message_id = message.get('message_id')
    user = message.get('from', {})
    username = user.get('username', user.get('first_name', 'Unknown'))
    chat_id = str(message['chat']['id'])
    
    # Auto-add user sebagai subscriber saat kirim command
    is_new_subscriber = add_subscriber(chat_id)
    if is_new_subscriber:
        welcome_msg = f"👋 Welcome {username}!\n\nYou have been subscribed to Kojin Bloomberg alerts."
        send_telegram_message(welcome_msg, chat_id)
    
    if text == '/start':
        if not monitoring_active:
            monitoring_active = True
            save_monitoring_status(True)
            response = f"🚀 Kojin Bloomberg Monitor Activated!\n\n" \
                      f"✅ Monitoring started by {username}\n" \
                      f"📧 Checking emails every 30 seconds\n" \
                      f"🔔 Headlines will be sent to all subscribers automatically\n" \
                      f"👥 Current subscribers: {len(subscribers)}\n\n" \
                      f"Commands:\n" \
                      f"• /status - Check status\n" \
                      f"• /unsubscribe - Stop receiving alerts\n" \
                      f"• /subscribers - Show subscriber count"
        else:
            response = f"ℹ️ Already Active\n\n" \
                      f"✅ Kojin Bloomberg monitoring is already running\n" \
                      f"👥 Current subscribers: {len(subscribers)}\n" \
                      f"💡 Use /unsubscribe to stop your personal alerts"
    elif text == '/status':
        if monitoring_active:
            last_data = get_last_email_data()
            if last_data:
                # Tampilkan headline lengkap tanpa dipotong
                last_headline = last_data[1]
                # Format waktu sesuai Bloomberg
                formatted_last_check = format_bloomberg_time(last_data[0])
                response = f"📊 Kojin Bloomberg Monitor Status\n\n" \
                          f"🟢 Status: Active\n" \
                          f"� Subscribers: {len(subscribers)}\n" \
                          f"�📧 Checking emails every 30 seconds\n" \
                          f"📰 Last News: {last_headline}\n" \
                          f"⏰ Last check: {formatted_last_check}"
            else:
                response = f"📊 Kojin Bloomberg Monitor Status\n\n" \
                          f"🟢 Status: Active\n" \
                          f"� Subscribers: {len(subscribers)}\n" \
                          f"�📧 Checking emails every 30 seconds\n" \
                          f"📰 No emails processed yet"
        else:
            response = f"📊 Kojin Bloomberg Monitor Status\n\n" \
                      f"🔴 Status: Stopped\n" \
                      f"👥 Subscribers: {len(subscribers)}\n" \
                      f"Use /start to activate monitoring"
    
    elif text == '/unsubscribe':
        if remove_subscriber(chat_id):
            response = f"👋 {username} have unsubscribed\n\n" \
                      f"❌ You will not receive Bloomberg alerts again\n" \
                      f"📝 Send /start to re-subscribe"
        else:
            response = f"ℹ️ You not subscribed yet\n\nSend /start to start receiving alerts"
    
    elif text == '/subscribers':
        response = f"👥 Subscriber Info\n\n" \
                  f"📊 Total subscribers: {len(subscribers)}\n" \
                  f"🤖 Bot: @cicilianews_bot\n" \
                  f"📧 Auto-subscribe when sending commands"
    
    elif text == '/test':
        # Format waktu current dalam format Bloomberg
        current_time_utc7 = datetime.utcnow() + timedelta(hours=7)
        current_bloomberg_time = current_time_utc7.strftime("%m/%d/%y %H:%M:%S UTC+7:00")
        
        response = f"🧪 Test Connection\n\n" \
                  f"✅ Bot is working correctly!\n" \
                  f"👤 User: {username}\n" \
                  f"🕐 Time: {current_bloomberg_time}\n" \
                  f"💬 Your Chat ID: {chat_id}\n" \
                  f"🤖 Bot: @cicilianews_bot"
    
    elif text == '/help':
        response = f"🤖 <b>Kojin Bloomberg Alert Bot</b>\n\n" \
                  f"📧 Kojin Monitors Bloomberg emails and sends headlines\n\n" \
                  f"<b>Commands:</b>\n" \
                  f"• /start - Start monitoring\n" \
                  f"• /status - Check current status\n" \
                  f"• /test - Test bot connection\n" \
                  f"• /unsubscribe - Stop receiving alerts\n" \
                  f"• /subscribers - Show subscriber count\n" \
                  f"• /help - Show this help\n\n" \
                  f"💡 Bot runs continuously once started"
    
    else:
        response = f"❓ <b>Unknown Command</b>\n\n" \
                  f"Use /help to see available commands"
    
    return send_telegram_message(response, chat_id=chat_id, reply_to_message_id=message_id)

def handle_callback_query(callback_query):
    """Handle callback query dari inline keyboard button"""
    try:
        query_id = callback_query['id']
        chat_id = str(callback_query['from']['id'])
        data = callback_query.get('data', '')
        
        # Answer callback query to remove loading state
        answer_callback_query(query_id)
        
        if data.startswith('show_ai:'):
            # Extract headline ID from callback data
            headline_id = data.split(':')[1]
            
            # Get AI analysis from cache
            if hasattr(broadcast_to_subscribers_with_ai, 'ai_cache'):
                ai_data = broadcast_to_subscribers_with_ai.ai_cache.get(headline_id)
                
                if ai_data:
                    headline = ai_data['headline']
                    analysis = ai_data['analysis']
                    
                    # Send AI analysis as new message with HTML formatting
                    ai_message = f"<b>🤖 AI Analysis:</b>\n\n{analysis}"
                    send_telegram_message(ai_message, chat_id)
                    print(f"📖 Sent AI analysis to {chat_id}")
                else:
                    send_telegram_message("❌ AI analysis not found or expired", chat_id, parse_mode=None)
            else:
                send_telegram_message("❌ AI analysis not available", chat_id, parse_mode=None)
                
    except Exception as e:
        print(f"❌ Error handling callback query: {e}")

def answer_callback_query(query_id, text=""):
    """Answer callback query to remove loading state"""
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/answerCallbackQuery"
        payload = {
            'callback_query_id': query_id,
            'text': text
        }
        response = requests.post(url, data=payload, timeout=5)
        return response.status_code == 200
    except Exception as e:
        print(f"❌ Error answering callback query: {e}")
        return False

def generate_ai_analysis(headline):
    """Generate AI analysis using Google Gemini API"""
    if not GEMINI_AVAILABLE:
        print("⚠️ Google Generative AI not installed")
        return None
    
    if not GEMINI_API_KEY or GEMINI_API_KEY == 'YOUR_GEMINI_KEY':
        print("❌ Gemini API key not configured")
        return None
    
    try:
        genai.configure(api_key=GEMINI_API_KEY)
        
        prompt = f"""Tolong bikin penjelasan berita dengan gaya Bloomberg/Reuters, panjang 2 paragraf. Gunakan headline berikut: {headline}

Paragraf pertama: jelaskan isi utama berita (siapa, apa, kapan, data/indikator utama kalau ada).
Paragraf kedua: jelaskan konteks, dampak, atau implikasi dari berita tersebut (misalnya ke pasar, kebijakan, atau tren yang lebih luas). 

Gunakan bahasa formal, padat, tapi tetap enak dibaca. Tulis dalam bahasa Indonesia."""

        # Try modern API first (if available)
        if hasattr(genai, 'GenerativeModel'):
            try:
                print("🔄 Using GenerativeModel API...")
                model = genai.GenerativeModel('gemini-pro')
                response = model.generate_content(prompt)
                if response and hasattr(response, 'text') and response.text:
                    analysis = response.text.strip()
                    print(f"✅ AI analysis generated ({len(analysis)} chars)")
                    return analysis
            except Exception as e:
                print(f"❌ GenerativeModel failed: {str(e)}")
        
        # Try legacy API (for older versions)
        try:
            print("🔄 Using legacy generate_text API...")
            response = genai.generate_text(
                model='models/text-bison-001',
                prompt=prompt,
                temperature=0.7,
                max_output_tokens=800
            )
            
            if response and hasattr(response, 'result') and response.result:
                analysis = response.result.strip()
                print(f"✅ AI analysis generated ({len(analysis)} chars)")
                return analysis
                
        except Exception as e:
            print(f"❌ Legacy API failed: {str(e)}")
        
        # Direct REST API fallback
        try:
            print("🔄 Using direct REST API...")
            import requests
            
            url = f"https://generativelanguage.googleapis.com/v1beta2/models/text-bison-001:generateText?key={GEMINI_API_KEY}"
            payload = {
                "prompt": {"text": prompt},
                "temperature": 0.7,
                "candidateCount": 1
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                result = response.json()
                if 'candidates' in result and result['candidates']:
                    candidate = result['candidates'][0]
                    if 'output' in candidate:
                        analysis = candidate['output'].strip()
                        print(f"✅ AI analysis generated ({len(analysis)} chars)")
                        return analysis
            else:
                print(f"❌ REST API failed: {response.status_code}")
                
        except Exception as e:
            print(f"❌ REST API failed: {str(e)}")
        
        print("❌ All AI methods failed")
        return None
            
    except Exception as e:
        print(f"❌ AI analysis error: {str(e)}")
        return None

def format_bloomberg_time(email_date_str):
    """Convert email date string to Bloomberg format like: 08/09/25 14:32:00 UTC+7:00"""
    try:
        # Parse email date string (format: "Sat, 9 Aug 2025 07:32:00 -0000")
        parsed_date = email.utils.parsedate_tz(email_date_str)
        
        if parsed_date:
            # Convert to datetime object
            dt = datetime(*parsed_date[:6])
            
            # Add timezone offset if exists
            if parsed_date[9]:
                dt = dt - timedelta(seconds=parsed_date[9])
            
            # Convert to UTC+7 (Bloomberg timezone for Asia)
            utc7_dt = dt + timedelta(hours=7)
            
            # Format like Bloomberg: MM/DD/YY HH:MM:SS UTC+7:00
            formatted = utc7_dt.strftime("%m/%d/%y %H:%M:%S UTC+7:00")
            return formatted
        else:
            # Fallback: current time in UTC+7
            now_utc7 = datetime.utcnow() + timedelta(hours=7)
            return now_utc7.strftime("%m/%d/%y %H:%M:%S UTC+7:00")
            
    except Exception as e:
        print(f"❌ Error parsing date: {e}")
        # Fallback: current time in UTC+7
        now_utc7 = datetime.utcnow() + timedelta(hours=7)
        return now_utc7.strftime("%m/%d/%y %H:%M:%S UTC+7:00")

def send_to_telegram(headline, date):
    """Broadcast headline Bloomberg ke semua subscribers dengan AI analysis"""
    try:
        # Format waktu sesuai dengan email Bloomberg
        formatted_time = format_bloomberg_time(date)
        
        # Generate AI analysis
        print(f"🤖 Generating AI analysis for: {headline[:50]}...")
        ai_analysis = generate_ai_analysis(headline)
        
        if ai_analysis:
            print(f"✅ AI analysis generated successfully ({len(ai_analysis)} chars)")
            # Format pesan utama dengan HTML bold formatting
            message = f"<b>🔔 Bloomberg Alert</b>\n\n" \
                     f"{headline}\n\n" \
                     f"{formatted_time}"
            
            # Broadcast ke semua subscribers dengan inline keyboard
            return broadcast_to_subscribers_with_ai(message, headline, ai_analysis)
        else:
            print("❌ AI analysis failed, sending simple alert")
            # Send simple alert without AI analysis button
            message = f"<b>🔔 Bloomberg Alert</b>\n\n" \
                     f"{headline}\n\n" \
                     f"{formatted_time}\n\n" \
                     f"<i>AI analysis unavailable</i>"
            
            return broadcast_to_subscribers(message)
            
    except Exception as e:
        print(f"❌ Error mengirim ke Telegram: {e}")
        return False

def save_last_email_data(email_data):
    """Menyimpan data email terakhir ke file JSON"""
    with open(LAST_EMAIL_DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(email_data, f)

def get_last_email_data():
    """Mengambil data email terakhir dari file JSON"""
    if os.path.exists(LAST_EMAIL_DATA_FILE):
        with open(LAST_EMAIL_DATA_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def get_gmail_service():
    """Menangani otentikasi dan mengembalikan objek layanan Gmail API"""
    creds = None
    
    # Try to load from environment variable first (for production)
    credentials_json = os.getenv('GOOGLE_CREDENTIALS_JSON')
    if credentials_json:
        import json
        
        # Parse JSON credentials from environment
        try:
            creds_info = json.loads(credentials_json)
            creds = Credentials.from_authorized_user_info(creds_info, SCOPES)
        except Exception as e:
            print(f"❌ Error parsing credentials from environment: {e}")
    
    # Fallback to local token.json file
    if not creds and os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
                # Save refreshed token back to environment in production
                if credentials_json:
                    print("✅ Token refreshed successfully")
            except Exception as e:
                print(f"❌ Error refreshing token: {e}")
                # In production, we can't do interactive auth, so exit
                if credentials_json:
                    print("❌ Cannot refresh token in production mode")
                    return None
        else:
            # Interactive auth only works locally
            if not credentials_json and os.path.exists('credentials.json'):
                flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
                with open('token.json', 'w') as token:
                    token.write(creds.to_json())
            else:
                print("❌ No valid credentials available in production mode")
                return None
                
    return build('gmail', 'v1', credentials=creds)

def get_last_processed_id():
    """Membaca ID email terakhir yang diproses dari file"""
    if os.path.exists(LAST_PROCESSED_ID_FILE):
        with open(LAST_PROCESSED_ID_FILE, 'r') as f:
            content = f.read().strip()
            return content if content else None
    return None

def save_last_processed_id(email_id):
    """Menyimpan ID email yang baru diproses ke file"""
    with open(LAST_PROCESSED_ID_FILE, 'w') as f:
        f.write(email_id)

def telegram_bot_listener():
    """Thread untuk mendengarkan commands dari Telegram"""
    global last_update_offset
    
    print("🤖 Telegram bot listener started...")
    processed_messages = set()  # Track processed message IDs
    processed_callbacks = set()  # Track processed callback query IDs
    
    while True:
        try:
            updates = get_telegram_updates(last_update_offset)
            
            if updates and updates.get('ok'):
                for update in updates.get('result', []):
                    last_update_offset = update['update_id'] + 1
                    
                    # Handle regular messages (commands)
                    if 'message' in update:
                        message = update['message']
                        message_id = message.get('message_id')
                        
                        # Skip if already processed
                        if message_id in processed_messages:
                            continue
                            
                        if 'text' in message and message['text'].startswith('/'):
                            print(f"📱 Received command: {message['text']}")
                            handle_telegram_command(message)
                            processed_messages.add(message_id)
                            
                            # Keep only recent 100 message IDs to prevent memory leak
                            if len(processed_messages) > 100:
                                processed_messages = set(list(processed_messages)[-50:])
                    
                    # Handle callback queries (button clicks)
                    elif 'callback_query' in update:
                        callback_query = update['callback_query']
                        callback_id = callback_query.get('id')
                        
                        # Skip if already processed
                        if callback_id in processed_callbacks:
                            continue
                            
                        print(f"📱 Received callback: {callback_query.get('data')}")
                        handle_callback_query(callback_query)
                        processed_callbacks.add(callback_id)
                        
                        # Keep only recent 100 callback IDs to prevent memory leak
                        if len(processed_callbacks) > 100:
                            processed_callbacks = set(list(processed_callbacks)[-50:])
            
            time.sleep(2)  # Check for updates every 2 seconds
            
        except Exception as e:
            print(f"❌ Error in telegram listener: {e}")
            time.sleep(5)  # Wait before retry

def check_bloomberg_emails():
    """Fungsi utama untuk mengecek email Bloomberg"""
    global monitoring_active
    
    if not monitoring_active:
        return False
    
    try:
        gmail_service = get_gmail_service()
        last_processed_id = get_last_processed_id()

        # Mencari satu email terbaru dari Bloomberg
        print("Mencari email dari Bloomberg...")
        results = gmail_service.users().messages().list(userId='me', q="bloomberg", maxResults=1).execute()
        messages = results.get('messages', [])
        print(f"Ditemukan {len(messages)} email dengan kata 'bloomberg'")

        if not messages:
            last_id = get_last_processed_id()
            last_data = get_last_email_data()
            if last_id and last_data:
                print(f"Tidak ada email baru. Data terakhir: {last_id}")
            else:
                print("Tidak ada email dari Bloomberg yang ditemukan.")
            return False

        latest_email_id = messages[0]['id']

        # Memeriksa apakah email terbaru sudah pernah diproses
        if latest_email_id == last_processed_id:
            print(f"Email terbaru sudah diproses: {latest_email_id}")
            return False

        # Jika email berbeda, proses email tersebut
        message = messages[0]
        msg = gmail_service.users().messages().get(userId='me', id=message['id'], format='full').execute()
        headers = msg['payload']['headers']
        
        # Ambil hanya subject (headline) dan tanggal
        subject = next((header['value'] for header in headers if header['name'] == 'Subject'), 'No Subject')
        date = next((header['value'] for header in headers if header['name'] == 'Date'), 'No Date')

        # Format data untuk backup: [Waktu, Headline]
        email_row = [date, subject]
        save_last_email_data(email_row)

        print(f"📧 Data email baru:")
        print(f"   Waktu: {date}")
        print(f"   Headline: {subject}")

        # Kirim headline ke Telegram
        if send_to_telegram(subject, date):
            print("✅ Headline berhasil dikirim ke Telegram")
            # Simpan ID email terbaru yang berhasil diproses
            save_last_processed_id(latest_email_id)
            print("🎉 Berhasil memproses email Bloomberg")
            return True
        else:
            print("❌ Gagal mengirim ke Telegram, tidak menyimpan ID")
            return False

    except HttpError as error:
        print(f'❌ Terjadi kesalahan API: {error}')
        return False
    except Exception as e:
        print(f'❌ Terjadi kesalahan umum: {e}')
        return False

def main():
    """Fungsi utama bot"""
    global monitoring_active
    
    print("🤖 Kojin Bloomberg Alert Bot Starting...")
    print("="*50)
    
    # Clear webhook untuk menghindari konflik
    print("🧹 Clearing any existing webhooks...")
    clear_webhook()
    
    # Load subscribers dan status monitoring dari file
    load_subscribers()
    monitoring_active = get_monitoring_status()
    
    if monitoring_active:
        print("✅ Monitoring was active, resuming...")
        send_telegram_message("🔄 <b>Bot Restarted</b>\n\nMonitoring resumed automatically")
    else:
        print("⏸️ Monitoring is inactive, waiting for /start command...")
        send_telegram_message("🤖 Kojin Bloomberg Bot Ready\n\nSend /start to begin monitoring Bloomberg emails")
    
    # Start Telegram bot listener in separate thread
    telegram_thread = threading.Thread(target=telegram_bot_listener, daemon=True)
    telegram_thread.start()
    
    print("🚀 Bot started! Listening for Telegram commands...")
    print("📱 Send /start to your bot to begin monitoring")
    print("🔍 Checking emails every 30 seconds when active")
    print("❌ Press Ctrl+C to stop")
    
    try:
        while True:
            if monitoring_active:
                check_bloomberg_emails()
            time.sleep(30)  # Check emails every 30 seconds
    except KeyboardInterrupt:
        print("\n🛑 Stopping bot...")
        monitoring_active = False
        save_monitoring_status(False)
        send_telegram_message("🛑 <b>Bot Stopped</b>\n\nMonitoring has been stopped manually")
        print("👋 Bot stopped!")

if __name__ == '__main__':
    main()
