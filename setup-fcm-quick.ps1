# Quick FCM Setup Guide - Web-Based (Easiest)
# Since Firebase requires browser auth, use the web console

Write-Host "🔥 Firebase FCM Quick Setup Guide" -ForegroundColor Cyan
Write-Host "=================================`n" -ForegroundColor Cyan

Write-Host "Since Firebase requires browser authentication, use the web console:`n" -ForegroundColor Yellow

Write-Host "STEP 1: Create Firebase Project" -ForegroundColor Cyan
Write-Host "-------------------------------" -ForegroundColor Cyan
Start-Process "https://console.firebase.google.com/"
Write-Host "✓ Opened Firebase Console" -ForegroundColor Green
Write-Host "  - Click 'Add project'" -ForegroundColor White
Write-Host "  - Name: rtx-stock-alert" -ForegroundColor White
Write-Host "  - Create project`n" -ForegroundColor White

Write-Host "STEP 2: Add Android App" -ForegroundColor Cyan
Write-Host "----------------------" -ForegroundColor Cyan
Write-Host "  - In Firebase Console → Add app → Android icon" -ForegroundColor White
Write-Host "  - Package name: com.rtxstock.alert" -ForegroundColor White
Write-Host "  - Register app" -ForegroundColor White
Write-Host "  - Download google-services.json (save for Android app)`n" -ForegroundColor White

Write-Host "STEP 3: Get Server Key" -ForegroundColor Cyan
Write-Host "----------------------" -ForegroundColor Cyan
Write-Host "  - Firebase Console → Project Settings (gear icon)" -ForegroundColor White
Write-Host "  - Cloud Messaging tab" -ForegroundColor White
Write-Host "  - Copy 'Server key' → This is FCM_SERVER_KEY`n" -ForegroundColor White

Write-Host "STEP 4: Get Device Token" -ForegroundColor Cyan
Write-Host "-----------------------" -ForegroundColor Cyan
Write-Host "  - Build Android app (see FCM_SETUP.txt for code)" -ForegroundColor White
Write-Host "  - Run app on your phone" -ForegroundColor White
Write-Host "  - App displays FCM token → Copy this (FCM_DEVICE_TOKEN)`n" -ForegroundColor White

Write-Host "STEP 5: Add to GitHub Secrets" -ForegroundColor Cyan
Write-Host "----------------------------" -ForegroundColor Cyan
Start-Process "https://github.com/sgpascoe/5090fe-stock-monitor/settings/secrets/actions"
Write-Host "✓ Opened GitHub Secrets page" -ForegroundColor Green
Write-Host "  - Click 'New repository secret'" -ForegroundColor White
Write-Host "  - Name: FCM_SERVER_KEY, Value: [your server key]" -ForegroundColor White
Write-Host "  - Click 'New repository secret' again" -ForegroundColor White
Write-Host "  - Name: FCM_DEVICE_TOKEN, Value: [your device token]`n" -ForegroundColor White

Write-Host "STEP 6: Test" -ForegroundColor Cyan
Write-Host "-----------" -ForegroundColor Cyan
Write-Host "  Run: .\test-fcm.ps1 -ServerKey 'YOUR_KEY' -DeviceToken 'YOUR_TOKEN'" -ForegroundColor White
Write-Host "  Or: python test_notifications.py`n" -ForegroundColor White

Write-Host "✅ Setup complete! Your FCM alerts are ready." -ForegroundColor Green

