# Bloomberg Alert Bot

Telegram bot yang memantau email Bloomberg dan mengirim notifikasi otomatis dengan AI analysis.

## ✨ Features
- 📧 **Auto Email Monitoring** - Monitor Bloomberg emails setiap 30 detik
- 🤖 **AI Analysis** - Analisis 2 paragraf otomatis dari headline
- � **Multi-subscriber** - Support multiple users
- 📱 **Commands** - Control via Telegram commands

## �🚀 Quick Setup

### 1. Setup Telegram Bot
```bash
python telegram_setup.py
```

### 2. Setup OpenAI (Opsional)
Edit `telegram_config.py` dan tambahkan OpenAI API key:
```python
OPENAI_API_KEY = "sk-your-openai-key"
```

### 3. Jalankan Bot
```bash
python bloomberg_simple.py
```

## 📋 Requirements
- Python 3.7+
- Gmail API credentials
- Telegram bot token

## 🔧 Commands
- `/start` - Mulai monitoring
- `/status` - Cek status
- `/unsubscribe` - Stop notifikasi
- `/help` - Bantuan

## 📁 File Structure
```
bloomberg/
├── bloomberg_simple.py    # Main application
├── telegram_setup.py      # Setup helper
├── telegram_config.py     # Config file (auto-generated)
├── requirements.txt       # Dependencies
└── README.md             # Documentation
```

## 🚀 Deployment
- Heroku
- Render 
- VPS/Server manual

## 🔒 Environment Variables
```
TELEGRAM_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
GOOGLE_CREDENTIALS_JSON=your_credentials_json
OPENAI_API_KEY=your_openai_key  # Opsional untuk AI analysis
```

## 📰 Message Format
```
🔔 Bloomberg Alert

📰 Fed's Goolsbee Says He Wants to See CPI Before Making Rate Call

🤖 AI Analysis:
[Paragraf 1: Isi utama berita...]
[Paragraf 2: Konteks dan dampak...]

⏰ 09/06/25 14:32:00 UTC+7:00
```
