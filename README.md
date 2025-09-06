# 🔔 Bloomberg Alert Bot

Bot Telegram yang memantau email Bloomberg dan mengirimkan alert otomatis dengan analisis AI.

## ✨ Features

- 📧 **Monitor email Bloomberg** otomatis
- 🤖 **AI Analysis** menggunakan Google Gemini
- 📱 **Telegram alerts** dengan format Bloomberg
- 👥 **Multi-subscriber** support
- ⚡ **Real-time notifications**

## 🚀 Quick Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Setup Gmail API
1. Buat project di [Google Cloud Console](https://console.cloud.google.com)
2. Enable Gmail API
3. Download `credentials.json`
4. Jalankan setup: `python telegram_setup.py`

### 3. Setup Telegram Bot
1. Chat dengan [@BotFather](https://t.me/botfather)
2. Buat bot baru dengan `/newbot`
3. Update `telegram_config.py`:
```python
TELEGRAM_TOKEN = "your_bot_token"
TELEGRAM_CHAT_ID = "your_chat_id"
GEMINI_API_KEY = "your_gemini_key"
```

### 4. Run Bot
```bash
python bloomberg_simple.py
```

## 📱 Commands

- `/start` - Start monitoring
- `/status` - Check status
- `/unsubscribe` - Stop receiving alerts
- `/help` - Show help

## 🔧 Configuration

Edit `telegram_config.py`:
```python
TELEGRAM_TOKEN = "your_telegram_bot_token"
TELEGRAM_CHAT_ID = "your_chat_id"  
GEMINI_API_KEY = "your_gemini_api_key"
```

## 📁 Project Structure

```
bloomberg-alert/
├── bloomberg_simple.py    # Main bot
├── telegram_config.py     # Configuration
├── telegram_setup.py      # Setup script
├── requirements.txt       # Dependencies
├── credentials.json       # Gmail API credentials
├── token.json            # Gmail API token
└── stop_bot.sh           # Stop script
```

## 💡 Tips

- Bot runs 24/7 once started
- Supports multiple subscribers
- AI analysis in Indonesian language
- Automatic error handling and retry
- Use `bash stop_bot.sh` to stop bot safely
