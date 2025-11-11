# Ultra-Quick Android App Setup
# Use Android Studio - it's fastest!

Write-Host "⚡ QUICKEST WAY - Use Android Studio GUI:" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

Write-Host "`n1. Open Android Studio" -ForegroundColor Yellow
Start-Process "https://developer.android.com/studio"

Write-Host "2. Create New Project:" -ForegroundColor Yellow
Write-Host "   - Template: Empty Activity" -ForegroundColor White
Write-Host "   - Name: RTX Stock Alert" -ForegroundColor White
Write-Host "   - Package: com.rtxstock.alert" -ForegroundColor White
Write-Host "   - Language: Java" -ForegroundColor White
Write-Host "   - Minimum SDK: API 26 (Android 8.0)" -ForegroundColor White

Write-Host "`n3. Add Firebase:" -ForegroundColor Yellow
Write-Host "   - Tools → Firebase → Cloud Messaging" -ForegroundColor White
Write-Host "   - Connect to Firebase" -ForegroundColor White
Write-Host "   - Select your project: rtx-stock-alert" -ForegroundColor White
Write-Host "   - Add FCM to your app" -ForegroundColor White

Write-Host "`n4. Copy google-services.json:" -ForegroundColor Yellow
Write-Host "   - Copy google-services.json to app/ folder" -ForegroundColor White

Write-Host "`n5. Replace MainActivity.java with code from FCM_SETUP.txt" -ForegroundColor Yellow

Write-Host "`n6. Add FirebaseMessagingService.java (from FCM_SETUP.txt)" -ForegroundColor Yellow

Write-Host "`n7. Update AndroidManifest.xml (add permissions from FCM_SETUP.txt)" -ForegroundColor Yellow

Write-Host "`n8. Build → Run on your phone" -ForegroundColor Yellow
Write-Host "   - App will display your FCM token" -ForegroundColor White
Write-Host "   - Copy that token!" -ForegroundColor White

Write-Host "`n✅ Done! Copy the FCM token to GitHub Secrets" -ForegroundColor Green

Write-Host "`n💡 Even faster: Use an existing FCM app like Pushbullet or Join!" -ForegroundColor Cyan

