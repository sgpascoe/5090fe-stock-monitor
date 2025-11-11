#!/usr/bin/env python3
"""
NVIDIA RTX 5090 FE Stock Monitor with Urgent Notifications
Checks NVIDIA UK store and sends multiple alert types when in stock
"""

import requests
import time
from datetime import datetime
import json
import os
from typing import Dict, Any

# Configuration - Use environment variables for cloud deployment
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "30"))  # seconds between checks
PRODUCT_NAME = "NVIDIA RTX 5090 FE"

# NVIDIA API endpoints
NVIDIA_API_URL = "https://api.nvidia.partners/edge/product/search?page=1&limit=9&locale=en-gb&category=GPU&gpu=RTX%205090"
NVIDIA_STORE_URL = "https://www.nvidia.com/en-gb/shop/geforce/gpu/?page=1&limit=100&locale=en-gb&category=GPU&gpu=RTX%205090"
NVIDIA_PRODUCT_PAGE = "https://www.nvidia.com/en-gb/geforce/graphics-cards/40-series/rtx-5090-5090ti/"

# Notification Services Configuration - from environment variables
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN", "")
PUSHOVER_USER = os.getenv("PUSHOVER_USER", "")

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK", "")

# IFTTT for multiple actions (phone call, smart home, etc)
IFTTT_KEY = os.getenv("IFTTT_KEY", "")
IFTTT_EVENT = os.getenv("IFTTT_EVENT", "rtx5090_in_stock")


class StockMonitor:
    def __init__(self):
        self.last_status = None
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'application/json',
            'Accept-Language': 'en-GB,en;q=0.9',
            'Referer': 'https://www.nvidia.com/en-gb/store/'
        })

    def check_stock(self) -> Dict[str, Any]:
        """Check NVIDIA store for RTX 5090 stock status using API and store page"""
        try:
            # Method 1: Try NVIDIA API endpoint
            try:
                api_response = self.session.get(NVIDIA_API_URL, timeout=10)
                if api_response.status_code == 200:
                    try:
                        data = api_response.json()
                        # Check if products exist and are available
                        if isinstance(data, dict) and "searchedProducts" in data:
                            products = data.get("searchedProducts", {}).get("productDetails", [])
                            for product in products:
                                product_name = product.get("productTitle", "").lower()
                                if "5090" in product_name and "founder" in product_name:
                                    # Check availability
                                    availability = product.get("prdStatus", "").lower()
                                    in_stock = "out of stock" not in availability and "notify me" not in availability
                                    if in_stock:
                                        price = product.get("productPrice", {}).get("finalPrice", "Check site")
                                        return {
                                            "in_stock": True,
                                            "timestamp": datetime.now().isoformat(),
                                            "url": NVIDIA_PRODUCT_PAGE,
                                            "price": price,
                                            "method": "api"
                                        }
                    except json.JSONDecodeError:
                        pass  # Fall through to HTML check
            except Exception as e:
                print(f"API check failed: {e}")
            
            # Method 2: Check store page HTML
            response = self.session.get(NVIDIA_STORE_URL, timeout=10)
            
            if response.status_code == 200:
                content = response.text.lower()
                
                # Look for stock indicators
                out_of_stock_indicators = [
                    "out of stock",
                    "notify me",
                    "coming soon",
                    "unavailable",
                    "sold out"
                ]
                
                in_stock_indicators = [
                    "add to cart",
                    "buy now",
                    "add to basket",
                    "purchase"
                ]
                
                has_out_of_stock = any(indicator in content for indicator in out_of_stock_indicators)
                has_in_stock = any(indicator in content for indicator in in_stock_indicators)
                
                # If we see in-stock indicators and no out-of-stock, it's likely available
                in_stock = has_in_stock and not has_out_of_stock
                
                return {
                    "in_stock": in_stock,
                    "timestamp": datetime.now().isoformat(),
                    "url": NVIDIA_PRODUCT_PAGE,
                    "price": "£1,799.00",  # Update if price changes
                    "method": "html"
                }
            else:
                return {
                    "in_stock": False,
                    "error": f"HTTP {response.status_code}",
                    "timestamp": datetime.now().isoformat()
                }
            
        except Exception as e:
            print(f"Error checking stock: {e}")
            return {"in_stock": False, "error": str(e), "timestamp": datetime.now().isoformat()}

    def send_pushover_emergency(self, message: str):
        """Send emergency Pushover notification that bypasses DND and repeats"""
        if PUSHOVER_TOKEN and PUSHOVER_USER:
            try:
                response = requests.post(
                    "https://api.pushover.net/1/messages.json",
                    data={
                        "token": PUSHOVER_TOKEN,
                        "user": PUSHOVER_USER,
                        "message": message,
                        "title": "🚨 RTX 5090 IN STOCK NOW!",
                        "priority": 2,  # Emergency priority
                        "retry": 30,    # Retry every 30 seconds
                        "expire": 3600, # Keep retrying for 1 hour
                        "sound": "persistent",  # Most annoying sound
                        "url": "https://www.nvidia.com/en-gb/shop/",
                        "url_title": "Open NVIDIA Store"
                    }
                )
                print(f"Pushover sent: {response.status_code}")
            except Exception as e:
                print(f"Pushover error: {e}")

    def send_telegram_urgent(self, message: str):
        """Send Telegram message with urgent formatting - sends multiple messages for maximum alert"""
        if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
            try:
                urgent_text = f"🚨🚨🚨 RTX 5090 IN STOCK NOW! 🚨🚨🚨\n\n{message}\n\n🚨 BUY NOW! 🚨"
                
                # Send 3 urgent messages in rapid succession for maximum alert
                for i in range(3):
                    response = requests.post(
                        f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage",
                        json={
                            "chat_id": TELEGRAM_CHAT_ID,
                            "text": urgent_text,
                            "parse_mode": "HTML",
                            "disable_notification": False,  # Ensure notification sound
                            "reply_markup": {
                                "inline_keyboard": [[
                                    {"text": "🚨 OPEN NVIDIA STORE NOW 🚨", "url": "https://www.nvidia.com/en-gb/shop/"}
                                ]]
                            }
                        }
                    )
                    print(f"Telegram message {i+1} sent: {response.status_code}")
                    if i < 2:  # Don't sleep after last message
                        time.sleep(1)  # 1 second between messages
            except Exception as e:
                print(f"Telegram error: {e}")

    def send_discord_alert(self, message: str):
        """Send Discord webhook with @everyone ping"""
        if DISCORD_WEBHOOK:
            try:
                response = requests.post(
                    DISCORD_WEBHOOK,
                    json={
                        "content": "@everyone",  # Ping everyone
                        "embeds": [{
                            "title": "🚨 RTX 5090 FE IN STOCK!",
                            "description": message,
                            "color": 0xFF0000,  # Red for urgency
                            "fields": [
                                {
                                    "name": "Direct Link",
                                    "value": "[CLICK HERE NOW](https://www.nvidia.com/en-gb/shop/)",
                                    "inline": False
                                }
                            ],
                            "timestamp": datetime.now().isoformat()
                        }]
                    }
                )
                print(f"Discord sent: {response.status_code}")
            except Exception as e:
                print(f"Discord error: {e}")

    def trigger_ifttt(self):
        """Trigger IFTTT applet for additional actions (phone call, lights, etc)"""
        if IFTTT_KEY:
            try:
                # Trigger multiple times for maximum alert
                for i in range(2):
                    response = requests.post(
                        f"https://maker.ifttt.com/trigger/{IFTTT_EVENT}/with/key/{IFTTT_KEY}",
                        json={
                            "value1": "🚨 RTX 5090 IN STOCK NOW! 🚨",
                            "value2": "https://www.nvidia.com/en-gb/shop/",
                            "value3": f"URGENT - {datetime.now().strftime('%H:%M:%S')}"
                        },
                        timeout=5
                    )
                    print(f"IFTTT trigger {i+1} sent: {response.status_code}")
                    if i < 1:
                        time.sleep(2)  # 2 seconds between triggers
            except Exception as e:
                print(f"IFTTT error: {e}")

    def send_all_alerts(self, stock_info: Dict[str, Any]):
        """Send alerts through all configured channels"""
        message = (
            f"RTX 5090 FE IS IN STOCK!\n"
            f"Time: {datetime.now().strftime('%H:%M:%S')}\n"
            f"Price: {stock_info.get('price', 'Check site')}\n"
            f"GO GO GO! → https://www.nvidia.com/en-gb/shop/"
        )
        
        # Send through all channels simultaneously
        self.send_pushover_emergency(message)
        self.send_telegram_urgent(message)
        self.send_discord_alert(message)
        self.trigger_ifttt()
        
        # Also print to console with bell character
        print("\a" * 5)  # System beep
        print("=" * 50)
        print(f"🚨🚨🚨 {message} 🚨🚨🚨")
        print("=" * 50)

    def run(self):
        """Main monitoring loop"""
        print(f"Starting RTX 5090 stock monitor...")
        print(f"Checking every {CHECK_INTERVAL} seconds")
        print(f"Current time: {datetime.now().strftime('%H:%M:%S')} UK")
        
        # Show configured notification services
        configured_services = []
        if PUSHOVER_TOKEN and PUSHOVER_USER:
            configured_services.append("Pushover")
        if TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
            configured_services.append("Telegram")
        if DISCORD_WEBHOOK:
            configured_services.append("Discord")
        if IFTTT_KEY:
            configured_services.append("IFTTT")
        
        if configured_services:
            print(f"Configured alerts: {', '.join(configured_services)}")
        else:
            print("⚠️  WARNING: No notification services configured! Set environment variables.")
        
        print("-" * 50)
        
        consecutive_errors = 0
        max_errors = 5
        
        while True:
            try:
                stock_info = self.check_stock()
                current_status = stock_info.get("in_stock", False)
                error = stock_info.get("error")
                
                if error:
                    consecutive_errors += 1
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] Error: {error} ({consecutive_errors}/{max_errors})")
                    if consecutive_errors >= max_errors:
                        print("⚠️  Too many consecutive errors. Waiting longer before retry...")
                        time.sleep(CHECK_INTERVAL * 5)
                        consecutive_errors = 0
                    else:
                        time.sleep(CHECK_INTERVAL)
                    continue
                else:
                    consecutive_errors = 0
                
                # Check if status changed to in stock
                if current_status and self.last_status != current_status:
                    print(f"\n🎯 STOCK DETECTED at {datetime.now().strftime('%H:%M:%S')}")
                    print(f"Method: {stock_info.get('method', 'unknown')}")
                    self.send_all_alerts(stock_info)
                    
                    # Keep alerting every minute while in stock
                    time.sleep(60)
                else:
                    status_msg = "In stock" if current_status else "Out of stock"
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] {status_msg} - checking again in {CHECK_INTERVAL}s...")
                
                self.last_status = current_status
                time.sleep(CHECK_INTERVAL)
                
            except KeyboardInterrupt:
                print("\nMonitoring stopped by user")
                break
            except Exception as e:
                consecutive_errors += 1
                print(f"Error in main loop: {e} ({consecutive_errors}/{max_errors})")
                if consecutive_errors >= max_errors:
                    print("⚠️  Too many consecutive errors. Waiting longer before retry...")
                    time.sleep(CHECK_INTERVAL * 5)
                    consecutive_errors = 0
                else:
                    time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    monitor = StockMonitor()
    monitor.run()
