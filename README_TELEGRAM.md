# 🤖 Bloomberg to Telegram Bot - Setup Guide

Script ini akan mengirim headline email Bloomberg langsung ke Telegram bot Anda.

## 🚀 Quick Start

### Step 1: Setup Telegram Bot
```bash
python telegram_setup.py
```

Ikuti instruksi di layar:
1. Buat bot baru dengan @BotFather
2. Dapatkan token bot
3. Kirim pesan ke bot
4. Jalankan script setup untuk auto-konfigurasi

### Step 2: Jalankan Bloomberg Monitor
```bash
python bloomberg_simple.py
```

## 📋 Manual Setup (jika diperlukan)

### 1. Buat Telegram Bot
1. Chat dengan @BotFather di Telegram
2. Kirim `/newbot`
3. Pilih nama bot (contoh: Bloomberg Alert Bot)
4. Pilih username bot (contoh: @your_bloomberg_bot)
5. Copy token yang diberikan

### 2. Dapatkan Chat ID
1. Kirim pesan ke bot yang baru dibuat
2. Buka: `https://api.telegram.org/bot<YOUR_TOKEN>/getUpdates`
3. Cari `"chat":{"id":` di response JSON
4. Copy angka ID tersebut

### 3. Update Konfigurasi
Edit file `telegram_config.py`:
```python
TELEGRAM_TOKEN = "123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZ"
TELEGRAM_CHAT_ID = "123456789"
```

## 🔧 Fitur

- ✅ **Monitoring Real-time**: Cek email Bloomberg setiap 30 detik
- ✅ **Headline Only**: Hanya kirim subject email (tanpa parsing body yang rumit)
- ✅ **Duplicate Prevention**: Tidak kirim email yang sama berulang kali
- ✅ **Telegram Formatting**: Pesan terformat rapi dengan emoji
- ✅ **Error Handling**: Retry otomatis jika ada error
- ✅ **Lightweight**: Minimal resource usage

## 📱 Format Pesan Telegram

```
🔔 Bloomberg Alert

📅 Waktu: Sat, 9 Aug 2025 05:03:05 -0000

📰 Headline:
The Bank of England Has Rarely Been This Split Over Inflation
```

## 🔍 Troubleshooting

### "Bot token invalid"
- Pastikan token dari @BotFather benar
- Token format: `123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghi`

### "Chat not found"
- Pastikan sudah kirim pesan ke bot minimal sekali
- Chat ID harus berupa angka (positif atau negatif)

### "No emails found"
- Pastikan ada email dari Bloomberg di Gmail
- Cek apakah Gmail API sudah enabled
- Pastikan token.json valid

### "Permission denied"
- Pastikan Gmail API dan token.json sudah disetup dengan benar
- Jalankan script sekali untuk login pertama kali

## 📁 File Structure

```
bloomberg/
├── bloomberg_simple.py      # Main script
├── telegram_setup.py        # Setup helper
├── telegram_config.py       # Config file (auto-generated)
├── credentials.json         # Google OAuth credentials
├── token.json              # Google access token
├── last_email_id.txt       # Tracking file
└── last_email_data.json    # Backup data
```

## 🚀 Deployment

Untuk deploy ke server/cloud:

1. **Railway (Recommended)**
2. **Render** 
3. **PythonAnywhere**
4. **Heroku**

Script ini bisa jalan 24/7 di cloud platform untuk monitoring otomatis.

## 🔒 Keamanan

- ❌ **Jangan commit** `telegram_config.py` ke Git
- ❌ **Jangan share** bot token di public
- ✅ **Gunakan** environment variables untuk production
- ✅ **Backup** file konfigurasi secara aman

## 🆘 Support

Jika ada masalah:
1. Cek error message di terminal
2. Pastikan semua file konfigurasi ada
3. Test Telegram bot dengan `telegram_setup.py`
4. Verify Gmail access dengan login manual
