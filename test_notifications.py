#!/usr/bin/env python3
"""
Quick test script to verify notifications work
Run this before deploying to test your notification setup
"""

import os
import sys
from nvidia_stock_monitor import StockMonitor

def test_notifications():
    """Test all configured notification services"""
    monitor = StockMonitor()
    
    # Show configured services
    configured = []
    if os.getenv("PUSHOVER_TOKEN") and os.getenv("PUSHOVER_USER"):
        configured.append("Pushover")
    if os.getenv("TELEGRAM_BOT_TOKEN") and os.getenv("TELEGRAM_CHAT_ID"):
        configured.append("Telegram")
    if os.getenv("DISCORD_WEBHOOK"):
        configured.append("Discord")
    if os.getenv("IFTTT_KEY"):
        configured.append("IFTTT")
    
    if not configured:
        print("[ERROR] No notification services configured!")
        print("Set at least one environment variable:")
        print("  - DISCORD_WEBHOOK (easiest)")
        print("  - TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID")
        print("  - PUSHOVER_TOKEN + PUSHOVER_USER")
        print("  - IFTTT_KEY")
        return False
    
    print(f"[OK] Testing notifications: {', '.join(configured)}")
    
    # Send test alert
    test_info = {
        "in_stock": True,
        "timestamp": "TEST",
        "url": "https://www.nvidia.com/en-gb/shop/",
        "price": "TEST - £1,799.00",
        "method": "test"
    }
    
    print("\nSending test alerts...")
    monitor.send_all_alerts(test_info)
    print("\n[OK] Test alerts sent! Check your notifications.")
    return True

if __name__ == "__main__":
    test_notifications()

