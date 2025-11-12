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
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# Monitor configuration
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "15"))  # seconds between checks (default 15s)
BACKOFF_DELAY = int(os.getenv("BACKOFF_DELAY", "5"))  # seconds to wait on error before retry
PRODUCT_NAME = "NVIDIA RTX 5090 FE"

# NVIDIA API endpoints
NVIDIA_API_URL = "https://api.nvidia.partners/edge/product/search?page=1&limit=9&locale=en-gb&category=GPU&gpu=RTX%205090"
NVIDIA_STORE_URL = "https://www.nvidia.com/en-gb/shop/geforce/gpu/?page=1&limit=100&locale=en-gb&category=GPU&gpu=RTX%205090"
NVIDIA_MARKETPLACE_URLS = [
    "https://marketplace.nvidia.com/en-gb/consumer/graphics-cards/nvidia-geforce-rtx-5090-borderlands-4-game-bundle/",
    "https://marketplace.nvidia.com/en-gb/consumer/graphics-cards/nvidia-geforce-rtx-5090/"
]
NVIDIA_PRODUCT_PAGE = NVIDIA_STORE_URL

# Notification Services Configuration - from environment variables
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN", "")
PUSHOVER_USER = os.getenv("PUSHOVER_USER", "")


class StockMonitor:
    def __init__(self):
        self.last_status = None
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/json",
            "Accept-Language": "en-GB,en;q=0.9",
            "Referer": "https://www.nvidia.com/en-gb/store/"
        })
        # Add retry strategy
        retry_strategy = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504],
            allowed_methods=["GET"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        self.session.mount("http://", adapter)
        self.session.mount("https://", adapter)

    def check_stock(self) -> Dict[str, Any]:
        """Check NVIDIA store for RTX 5090 stock status using API and multiple marketplace urls"""
        # Method 1: NVIDIA API
        try:
            api_response = self.session.get(NVIDIA_API_URL, timeout=(10, 30))  # (connect, read) timeout
            if api_response.status_code == 200:
                try:
                    data = api_response.json()
                except json.JSONDecodeError:
                    print("NVIDIA API returned invalid JSON, falling back to HTML scraping.")
                else:
                    products = data.get("searchedProducts", {}).get("productDetails", [])
                    for product in products:
                        product_name = (product.get("productTitle") or "").lower()
                        if "5090" in product_name and "founder" in product_name:
                            availability = (product.get("prdStatus") or "").lower()
                            in_stock = "out of stock" not in availability and "notify me" not in availability
                            if in_stock:
                                price = product.get("productPrice", {}).get("finalPrice", "Check site")
                                return {
                                    "in_stock": True,
                                    "timestamp": datetime.now().isoformat(),
                                    "url": product.get("productURL", NVIDIA_PRODUCT_PAGE),
                                    "price": price,
                                    "method": "api"
                                }
            else:
                print(f"NVIDIA API HTTP {api_response.status_code}")
        except Exception as exc:
            print(f"API check failed: {exc}")

        # Method 2: Marketplace pages (primary)
        out_of_stock_indicators = [
            "out of stock",
            "notify me",
            "coming soon",
            "unavailable",
            "sold out",
            "notify when available"
        ]
        in_stock_indicators = [
            "add to cart",
            "buy now",
            "add to basket",
            "purchase",
            "add to bag"
        ]

        marketplace_errors = []
        for url in NVIDIA_MARKETPLACE_URLS:
            try:
                response = self.session.get(url, timeout=(10, 30))  # (connect, read) timeout
            except Exception as exc:
                msg = f"{url} request failed: {exc}"
                print(msg)
                marketplace_errors.append(msg)
                continue

            if response.status_code != 200:
                msg = f"{url} HTTP {response.status_code}"
                print(msg)
                marketplace_errors.append(msg)
                continue

            content = response.text.lower()
            has_out_of_stock = any(indicator in content for indicator in out_of_stock_indicators)
            has_in_stock = any(indicator in content for indicator in in_stock_indicators)
            in_stock = has_in_stock and not has_out_of_stock

            if in_stock:
                return {
                    "in_stock": True,
                    "timestamp": datetime.now().isoformat(),
                    "url": url,
                    "price": "£1,799.00",
                    "method": "marketplace"
                }

        if marketplace_errors and len(marketplace_errors) == len(NVIDIA_MARKETPLACE_URLS):
            return {
                "in_stock": False,
                "error": "; ".join(marketplace_errors),
                "timestamp": datetime.now().isoformat()
            }

        return {
            "in_stock": False,
            "timestamp": datetime.now().isoformat(),
            "url": NVIDIA_PRODUCT_PAGE,
            "price": "£1,799.00",
            "method": "marketplace"
        }

    def send_pushover_emergency(self, message: str, url: str):
        """Send emergency Pushover notification that bypasses DND and repeats"""
        if not (PUSHOVER_TOKEN and PUSHOVER_USER):
            print("⚠️  Pushover credentials not configured.")
            return

        try:
            response = requests.post(
                "https://api.pushover.net/1/messages.json",
                data={
                    "token": PUSHOVER_TOKEN,
                    "user": PUSHOVER_USER,
                    "message": message,
                    "title": f"🚨 {PRODUCT_NAME} IN STOCK NOW!",
                    "priority": 2,  # Emergency priority
                    "retry": 30,    # Retry every 30 seconds
                    "expire": 3600, # Keep retrying for 1 hour
                    "sound": "persistent",
                    "url": url,
                    "url_title": "Open NVIDIA Store"
                },
                timeout=(10, 30)  # (connect, read) timeout
            )
            print(f"Pushover sent: {response.status_code}")
        except Exception as exc:
            print(f"Pushover error: {exc}")

    def send_small_alert(self, message: str):
        """Send a low-priority heads-up via Pushover and console"""
        print(f"[notice] {message}")
        if not (PUSHOVER_TOKEN and PUSHOVER_USER):
            return

        try:
            requests.post(
                "https://api.pushover.net/1/messages.json",
                data={
                    "token": PUSHOVER_TOKEN,
                    "user": PUSHOVER_USER,
                    "message": message,
                    "title": f"{PRODUCT_NAME} monitor",
                    "priority": 0,
                    "sound": "gamelan"
                },
                timeout=(10, 30)  # (connect, read) timeout
            )
        except Exception as exc:
            print(f"Pushover notice error: {exc}")

    def send_all_alerts(self, stock_info: Dict[str, Any]):
        """Send alerts through the configured channel"""
        url = stock_info.get("url", NVIDIA_PRODUCT_PAGE)
        price = stock_info.get("price", "Check site")
        message = (
            f"{PRODUCT_NAME} IS IN STOCK!\n"
            f"Time: {datetime.now().strftime('%H:%M:%S')}\n"
            f"Price: {price}\n"
            f"Link: {url}"
        )

        self.send_pushover_emergency(message, url)

        # Also print to console with bell character
        print("\a" * 5)  # System beep
        print("=" * 50)
        print(f"🚨🚨🚨 {message} 🚨🚨🚨")
        print("=" * 50)

    def run(self):
        """Main monitoring loop"""
        print(f"Starting {PRODUCT_NAME} stock monitor...")
        print(f"Checking every {CHECK_INTERVAL} seconds")
        print(f"Current time: {datetime.now().strftime('%H:%M:%S')} UK")

        if PUSHOVER_TOKEN and PUSHOVER_USER:
            print("Configured alerts: Pushover")
        else:
            print("⚠️  WARNING: Pushover not configured - no notifications will fire.")

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
                    error_msg = f"[{datetime.now().strftime('%H:%M:%S')}] Error: {error} ({consecutive_errors}/{max_errors})"
                    print(error_msg)

                    if consecutive_errors == 1:
                        self.send_small_alert(f"Monitor error: {error}. Retrying in {BACKOFF_DELAY}s...")
                    elif consecutive_errors >= max_errors:
                        self.send_small_alert(f"Multiple errors ({consecutive_errors}). Backing off for {CHECK_INTERVAL * 5}s...")

                    if consecutive_errors >= max_errors:
                        print(f"⚠️  Too many consecutive errors. Backing off for {CHECK_INTERVAL * 5}s...")
                        time.sleep(CHECK_INTERVAL * 5)
                        consecutive_errors = 0
                    else:
                        time.sleep(BACKOFF_DELAY)
                    continue
                else:
                    consecutive_errors = 0

                if current_status and self.last_status != current_status:
                    print(f"\n🎯 STOCK DETECTED at {datetime.now().strftime('%H:%M:%S')}")
                    print(f"Method: {stock_info.get('method', 'unknown')}")
                    self.send_all_alerts(stock_info)
                else:
                    status_msg = "In stock" if current_status else "Out of stock"
                    print(f"[{datetime.now().strftime('%H:%M:%S')}] {status_msg} - checking again in {CHECK_INTERVAL}s...")

                self.last_status = current_status
                time.sleep(CHECK_INTERVAL)

            except KeyboardInterrupt:
                print("\nMonitoring stopped by user")
                break
            except Exception as exc:
                consecutive_errors += 1
                error_msg = f"Error in main loop: {exc} ({consecutive_errors}/{max_errors})"
                print(error_msg)

                if consecutive_errors == 1:
                    self.send_small_alert(f"Monitor exception: {str(exc)[:100]}. Backing off {BACKOFF_DELAY}s...")
                elif consecutive_errors >= max_errors:
                    self.send_small_alert(f"Multiple exceptions ({consecutive_errors}). Backing off {CHECK_INTERVAL * 5}s...")

                if consecutive_errors >= max_errors:
                    print(f"⚠️  Too many consecutive errors. Backing off for {CHECK_INTERVAL * 5}s...")
                    time.sleep(CHECK_INTERVAL * 5)
                    consecutive_errors = 0
                else:
                    time.sleep(BACKOFF_DELAY)


if __name__ == "__main__":
    monitor = StockMonitor()
    monitor.run()
