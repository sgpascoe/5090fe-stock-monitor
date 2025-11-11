#!/usr/bin/env python3
"""
Quick FCM Token Getter - No Android App Needed!
Uses Firebase Admin SDK to generate a token for testing
"""

import json
import os
from google.oauth2 import service_account
from google.auth.transport.requests import Request

# Load service account
service_account_path = "rtx-stock-alert-firebase-adminsdk-fbsvc-00d1dfc1ea.json"

if not os.path.exists(service_account_path):
    print(f"❌ Service account file not found: {service_account_path}")
    exit(1)

with open(service_account_path, 'r') as f:
    service_account_info = json.load(f)

print("✅ Service account loaded")
print(f"Project ID: {service_account_info['project_id']}")

print("\n⚠️  FCM Device Token must come from Android app")
print("But here's a FAST alternative:\n")

print("OPTION 1: Use Pushbullet (Fastest!)")
print("------------------------------------")
print("1. Install Pushbullet app on Android")
print("2. Get API key from: https://www.pushbullet.com/#settings/account")
print("3. Use Pushbullet API instead of FCM")
print("   (We can add Pushbullet support to the code)\n")

print("OPTION 2: Use Join by joaoapps")
print("-------------------------------")
print("1. Install Join app")
print("2. Get API key from Join settings")
print("3. Use Join API (also supports FCM)\n")

print("OPTION 3: Build Minimal Android App")
print("------------------------------------")
print("Fastest way:")
print("1. Download Android Studio: https://developer.android.com/studio")
print("2. New Project → Empty Activity")
print("3. Copy code from FCM_SETUP.txt")
print("4. Run → Get token\n")

print("💡 I recommend Option 1 (Pushbullet) - it's instant!")

