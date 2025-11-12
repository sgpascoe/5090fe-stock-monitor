#!/usr/bin/env python3
"""
One-time stock check for GitHub Actions
Runs a single check and exits (no continuous loop)
"""

import sys
import os
from datetime import datetime

# Import the StockMonitor class
sys.path.insert(0, os.path.dirname(__file__))
from nvidia_stock_monitor import StockMonitor

if __name__ == "__main__":
    monitor = StockMonitor()
    
    # Check notification services configuration
    has_notifications = False
    if os.getenv("PUSHOVER_TOKEN") and os.getenv("PUSHOVER_USER"):
        has_notifications = True
    if os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("TELEGRAM_CHAT_ID"):
        has_notifications = True
    if os.getenv("DISCORD_WEBHOOK"):
        has_notifications = True
    if os.getenv("IFTTT_KEY"):
        has_notifications = True
    if os.getenv("TWILIO_ACCOUNT_SID") and os.getenv("TWILIO_AUTH_TOKEN"):
        has_notifications = True
    if os.getenv("FCM_SERVICE_ACCOUNT_JSON") and os.getenv("FCM_PROJECT_ID") and os.getenv("FCM_DEVICE_TOKEN"):
        has_notifications = True
    
    if not has_notifications:
        print("[WARNING] No notification services configured! Set GitHub Secrets.")
    
    # Run a single check
    print(f"[{datetime.now().strftime('%H:%M:%S')}] Checking stock...")
    stock_info = monitor.check_stock()
    current_status = stock_info.get("in_stock", False)
    error = stock_info.get("error")
    
    if error:
        print(f"[ERROR] Error checking stock: {error}")
        # Don't fail the workflow on network errors - just log and exit gracefully
        # This allows the workflow to continue running on the next scheduled run
        print("[INFO] Workflow will retry on next scheduled run")
        sys.exit(0)
    
    if current_status:
        print(f"[STOCK DETECTED] at {datetime.now().strftime('%H:%M:%S')}!")
        print(f"Method: {stock_info.get('method', 'unknown')}")
        print(f"Price: {stock_info.get('price', 'Check site')}")
        print(f"URL: {stock_info.get('url', '')}")
        monitor.send_all_alerts(stock_info)
        sys.exit(0)
    else:
        print(f"[OUT OF STOCK] (checked at {datetime.now().strftime('%H:%M:%S')})")
        sys.exit(0)

