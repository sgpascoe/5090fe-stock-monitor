#!/usr/bin/env python3
"""
Quick test script to verify notifications work
Run this before deploying to test your notification setup
"""

import os
import sys
from nvidia_stock_monitor import StockMonitor

def test_notifications():
    """Test Pushover notification service"""
    monitor = StockMonitor()
    
    # Check Pushover configuration
    has_pushover = os.getenv("PUSHOVER_TOKEN") and os.getenv("PUSHOVER_USER")
    
    if not has_pushover:
        print("[ERROR] Pushover not configured!")
        print("Set environment variables:")
        print("  - PUSHOVER_TOKEN")
        print("  - PUSHOVER_USER")
        return False
    
    print("[OK] Testing Pushover notifications...")
    
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

