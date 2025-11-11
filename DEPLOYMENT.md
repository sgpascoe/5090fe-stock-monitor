# NVIDIA RTX 5090 FE Stock Monitor - Deployment Guide

## 🚀 Quick Deploy to Render (Free Tier)

### Step 1: Create Render Account
1. Go to https://render.com
2. Sign up with GitHub (recommended) or email
3. Free tier includes 750 hours/month of worker time

### Step 2: Deploy from GitHub
1. Push this repository to GitHub
2. In Render dashboard, click "New +" → "Background Worker"
3. Connect your GitHub repository
4. Configure:
   - **Name**: `nvidia-stock-monitor`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python nvidia_stock_monitor.py`
   - **Plan**: `Free`

### Step 3: Set Environment Variables
In Render dashboard → Your service → Environment:
- Add at least ONE notification service:
  - `DISCORD_WEBHOOK` (easiest - free)
  - `TELEGRAM_BOT_TOKEN` + `TELEGRAM_CHAT_ID` (free)
  - `PUSHOVER_TOKEN` + `PUSHOVER_USER` (€5 one-time)
  - `IFTTT_KEY` (free)

Optional:
- `CHECK_INTERVAL` (default: 30 seconds)
- `IFTTT_EVENT` (default: rtx5090_in_stock)

### Step 4: Deploy!
Click "Create Background Worker" and it will start monitoring!

---

## 📱 Setting Up Notifications (Choose at least one)

### Discord (Easiest - Free)
1. Create a Discord server (or use existing)
2. Server Settings → Integrations → Webhooks → New Webhook
3. Copy webhook URL
4. Add as `DISCORD_WEBHOOK` environment variable

### Telegram (Free)
1. Message @BotFather on Telegram → `/newbot`
2. Follow instructions to create bot
3. Get bot token → Set as `TELEGRAM_BOT_TOKEN`
4. Message @userinfobot → Get your chat ID → Set as `TELEGRAM_CHAT_ID`
5. Start a chat with your bot (important!)

### Pushover (€5 one-time - Best for urgent alerts)
1. Download Pushover app (iOS/Android)
2. Create account at https://pushover.net
3. Get API token → Set as `PUSHOVER_TOKEN`
4. Get user key → Set as `PUSHOVER_USER`
5. Enables emergency alerts that bypass Do Not Disturb!

### IFTTT (Free - Can trigger phone calls, lights, etc)
1. Go to https://ifttt.com/maker_webhooks
2. Get your webhook key → Set as `IFTTT_KEY`
3. Create applets like:
   - IF webhook triggered → Call my phone
   - IF webhook triggered → Flash smart lights
   - IF webhook triggered → Send SMS

---

## 🔄 Alternative Free Deployments

### Railway (Free Tier)
1. Go to https://railway.app
2. New Project → Deploy from GitHub
3. Add environment variables
4. Free tier: $5 credit/month

### PythonAnywhere (Free Tier)
1. Sign up at https://www.pythonanywhere.com
2. Upload files via Files tab
3. Run in Bash console: `python3.10 nvidia_stock_monitor.py`
4. Free tier: Limited CPU time, but works for monitoring

### GitHub Actions (Free - Runs on schedule)
Create `.github/workflows/stock-check.yml`:
```yaml
name: RTX 5090 Stock Check
on:
  schedule:
    - cron: '*/1 * * * *'  # Every minute
  workflow_dispatch:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - run: pip install -r requirements.txt
      - run: python nvidia_stock_monitor.py
        env:
          DISCORD_WEBHOOK: ${{ secrets.DISCORD_WEBHOOK }}
          # Add other secrets as needed
```

---

## ✅ Verify It's Working

1. Check Render logs - should see:
   ```
   Starting RTX 5090 stock monitor...
   Checking every 30 seconds
   Configured alerts: Discord
   ```

2. Test notifications by temporarily modifying the script to send a test alert

3. Monitor will run 24/7 and alert immediately when stock is detected!

---

## 🎯 Tips

- **Check interval**: 30 seconds is good balance (too fast = risk of IP ban)
- **Multiple alerts**: Set up 2+ notification methods for redundancy
- **Mobile**: Keep Discord/Telegram notifications enabled on your phone
- **Free tier limits**: Render free tier sleeps after 15 min inactivity, but wakes on activity (checks count as activity)

---

## 🆘 Troubleshooting

**Service stops after 15 minutes?**
- Render free tier sleeps but wakes on activity
- Checks every 30s keep it awake
- If it sleeps, it will wake on next check

**No notifications?**
- Check environment variables are set correctly
- Check Render logs for errors
- Test notification service separately

**Too many errors?**
- Script auto-handles temporary network issues
- After 5 consecutive errors, waits longer before retry

