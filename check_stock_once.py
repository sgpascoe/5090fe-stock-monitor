#!/usr/bin/env python3
"""
One-time stock check for GitHub Actions
Runs a single check and exits (no continuous loop)
"""

import sys
import os
from datetime import datetime

# Import the StockMonitor class and notification config
sys.path.insert(0, os.path.dirname(__file__))
from nvidia_stock_monitor import (
    StockMonitor,
    PUSHOVER_TOKEN,
    PUSHOVER_USER,
    TELEGRAM_BOT_TOKEN,
    TELEGRAM_CHAT_ID,
    DISCORD_WEBHOOK,
    IFTTT_KEY,
    TWILIO_ACCOUNT_SID,
    TWILIO_AUTH_TOKEN,
    FCM_SERVER_KEY,
    FCM_DEVICE_TOKEN
)

if __name__ == "__main__":
    monitor = StockMonitor()
    
    # Check notification services configuration
    has_notifications = False
    if PUSHOVER_TOKEN and PUSHOVER_USER:
        has_notifications = True
    if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        has_notifications = True
    if DISCORD_WEBHOOK:
        has_notifications = True
    if IFTTT_KEY:
        has_notifications = True
    if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
        has_notifications = True
    if FCM_SERVER_KEY and FCM_DEVICE_TOKEN:
        has_notifications = True
    
    if not has_notifications:
        print("⚠️  WARNING: No notification services configured! Set GitHub Secrets.")
    
    # Run a single check
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking stock...")
    stock_info = monitor.check_stock()
    current_status = stock_info.get("in_stock", False)
    error = stock_info.get("error")
    
    if error:
        print(f"❌ Error checking stock: {error}")
        sys.exit(1)
    
    if current_status:
        print(f"🎯 STOCK DETECTED at {datetime.now().strftime('%H:%M:%S')}!")
        print(f"Method: {stock_info.get('method', 'unknown')}")
        print(f"Price: {stock_info.get('price', 'Check site')}")
        print(f"URL: {stock_info.get('url', '')}")
        monitor.send_all_alerts(stock_info)
        sys.exit(0)
    else:
        print(f"📦 Out of stock (checked at {datetime.now().strftime('%H:%M:%S')})")
        sys.exit(0)

