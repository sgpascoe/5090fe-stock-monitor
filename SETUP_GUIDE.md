# RTX 5090 Stock Alert Setup Guide

## 🚨 Making Notifications TRULY Unignorable

### iPhone Setup (Most Aggressive)

1. **Using Pushover (Recommended - £4.99 once)**
   - Download Pushover app from App Store
   - In Settings → Notifications → Pushover:
     - Allow Notifications: ON
     - Critical Alerts: ON (this bypasses DND/Silent!)
     - Sounds: Persistent (loudest)
     - Show in CarPlay: ON
   - Emergency priority messages will:
     - Bypass Do Not Disturb
     - Repeat every 30 seconds until acknowledged
     - Play sound even on silent mode

2. **iOS Shortcuts Method (Free)**
   ```
   Create shortcut that:
   1. Checks stock API every 5 minutes
   2. If in stock:
      - Set volume to 100%
      - Play alarm sound 5 times
      - Flash torch
      - Send notification
      - Open NVIDIA store
   ```

### Android Setup (More Options)

1. **Tasker + Join (Most Powerful)**
   - Tasker can override all phone settings
   - Create profile that:
     - Sets volume to max
     - Plays custom alarm
     - Vibrates continuously
     - Flashes screen
     - Opens browser automatically

2. **Using Telegram**
   - Create bot and set custom notification sound
   - In Android settings for Telegram:
     - Override Do Not Disturb: Yes
     - Sound: Custom loud alarm
     - Pop on screen: Yes
     - Use high priority: Yes

## 🎯 Quick Win Services (No Coding)

### HotStock App Settings:
- Product: NVIDIA RTX 5090 FE
- Retailer: NVIDIA UK Store
- Alert Type: Push + Sound + Vibration
- Alert Sound: Air Horn (loudest)
- Repeat Alert: Every 30 seconds

### Discord Stock Servers:
1. Join servers:
   - PartAlert UK
   - FE Stock Alerts
   - StockDrops UK

2. Mobile notification setup:
   - Server Settings → Notifications → All Messages
   - Override default: ON  
   - Notification Settings → Direct Messages → Push Notifications: Always
   - Suppress @everyone: OFF (important!)

## 💻 Running the Python Script 24/7

### Option A: Cloud VPS (Always On)
```bash
# On a cheap VPS (£3/month) or free Oracle Cloud
git clone [your-repo]
pip install -r requirements.txt
nohup python3 nvidia_stock_monitor.py &
```

### Option B: Raspberry Pi at Home
```bash
# Set up as systemd service for auto-restart
sudo nano /etc/systemd/system/rtx-monitor.service

[Unit]
Description=RTX 5090 Stock Monitor
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/stock-monitor
ExecStart=/usr/bin/python3 /home/pi/stock-monitor/nvidia_stock_monitor.py
Restart=always

[Install]
WantedBy=multi-user.target

# Enable service
sudo systemctl enable rtx-monitor
sudo systemctl start rtx-monitor
```

### Option C: GitHub Actions (Free)
```yaml
# .github/workflows/stock-check.yml
name: RTX 5090 Stock Check
on:
  schedule:
    - cron: '*/5 * * * *'  # Every 5 minutes
  workflow_dispatch:

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Check Stock
        run: |
          python check_stock.py
        env:
          PUSHOVER_TOKEN: ${{ secrets.PUSHOVER_TOKEN }}
          PUSHOVER_USER: ${{ secrets.PUSHOVER_USER }}
```

## 🔊 Maximum Alert Setup

### Combine Multiple Methods:
1. **Pushover** - Emergency alerts that bypass everything
2. **IFTTT** - Trigger phone call to yourself
3. **Smart Home** - Flash all lights red
4. **Discord** - Desktop + mobile notifications
5. **Browser Extension** - Distill Web Monitor

### Nuclear Option - IFTTT Recipes:
- IF stock found THEN call my phone
- IF stock found THEN flash Philips Hue lights
- IF stock found THEN send SMS to 5 friends
- IF stock found THEN play siren on Alexa
- IF stock found THEN email with high importance

## ⚡ Testing Your Setup

Test your alerts work BEFORE stock appears:
```python
# Test notification in Python script
monitor = StockMonitor()
monitor.send_all_alerts({"in_stock": True, "price": "TEST"})
```

## 📱 Battle-Tested Settings

From successful buyers:
- Check interval: 30 seconds (not faster to avoid bans)
- Run from 10 AM - 5 PM UK time primarily
- Keep payment info saved in NVIDIA account
- Use NVIDIA app on phone (sometimes faster)
- Have backup payment methods ready
- Be logged into NVIDIA store already

## Important Notes:
1. Stock typically lasts only **minutes to hours**
2. Most restocks happen **11 AM - 4 PM UK time**
3. Mobile app sometimes has stock when website doesn't
4. Keep multiple tabs open (UK, DE, FR stores)
5. Use PayPal express checkout if available (faster)

Ready to deploy? Pick at least 2 methods above for redundancy!