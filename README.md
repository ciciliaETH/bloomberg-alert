# Bloomberg Alert Bot - Railway Deployment

## 🚀 Quick Deploy to Railway

### 1. Prerequisites
- GitHub account
- Railway account (https://railway.app)
- Google Gmail API credentials
- Telegram bot token

### 2. Setup Steps

#### Step 1: Push to GitHub
```bash
git init
git add .
git commit -m "Initial Bloomberg bot commit"
git branch -M main
git remote add origin https://github.com/yourusername/bloomberg-bot.git
git push -u origin main
```

#### Step 2: Deploy to Railway
1. Go to https://railway.app
2. Click "Start a New Project"
3. Choose "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect Python and start building

#### Step 3: Set Environment Variables
In Railway dashboard, go to Variables tab and add:

```
TELEGRAM_TOKEN=8122220616:AAFI8xFd2O0X1UiJWBWvO8j5-pgeysLCbpc
TELEGRAM_CHAT_ID=YOUR_CHAT_ID
GOOGLE_CREDENTIALS_JSON={"token": "...", "refresh_token": "...", "token_uri": "...", "client_id": "...", "client_secret": "...", "scopes": ["..."]}
```

#### Step 4: Get Google Credentials JSON
1. Run locally: `python bloomberg_simple.py`
2. Complete OAuth flow
3. Copy content of `token.json`
4. Minify JSON (remove spaces/newlines)
5. Add to Railway as `GOOGLE_CREDENTIALS_JSON`

### 3. Files Structure
```
bloomberg/
├── bloomberg_simple.py    # Main bot code
├── telegram_config.py     # Local config (gitignored)
├── requirements.txt       # Python dependencies
├── Procfile              # Railway process definition
├── railway.json          # Railway configuration
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

### 4. Bot Commands
- `/start` - Start monitoring
- `/status` - Check status
- `/test` - Test connection
- `/unsubscribe` - Stop personal alerts
- `/subscribers` - Show subscriber count
- `/help` - Show help

### 5. Features
- ✅ Multi-user support with auto-subscribe
- ✅ Persistent subscriber storage
- ✅ Email monitoring every 30 seconds
- ✅ Auto-restart on crash
- ✅ Production-ready with environment variables

### 6. Monitoring
- Check Railway logs for errors
- Bot auto-restarts on failure
- Use `/status` command to verify operation

### 7. Cost Estimate
- Railway Free: 500 execution hours/month
- Expected usage: ~720 hours/month for 24/7
- Upgrade to Pro ($5/month) for unlimited hours

## 🔧 Local Development
```bash
pip install -r requirements.txt
python bloomberg_simple.py
```
