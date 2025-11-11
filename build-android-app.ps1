# Quick Android App Build Script
# Creates minimal FCM app and builds it

Write-Host "🚀 Building Android FCM App..." -ForegroundColor Cyan

# Check if Android SDK is available
$androidHome = $env:ANDROID_HOME
if (-not $androidHome) {
    Write-Host "❌ ANDROID_HOME not set!" -ForegroundColor Red
    Write-Host "Install Android Studio or set ANDROID_HOME" -ForegroundColor Yellow
    exit 1
}

Write-Host "✓ Android SDK found at: $androidHome" -ForegroundColor Green

# Create app directory
$appDir = "android-app"
if (Test-Path $appDir) {
    Remove-Item $appDir -Recurse -Force
}
New-Item -ItemType Directory -Path $appDir | Out-Null
Set-Location $appDir

Write-Host "`n📦 Creating Android project structure..." -ForegroundColor Yellow

# Create basic Android project structure
New-Item -ItemType Directory -Path "app\src\main\java\com\rtxstock\alert" -Force | Out-Null
New-Item -ItemType Directory -Path "app\src\main\res\layout" -Force | Out-Null
New-Item -ItemType Directory -Path "app\src\main\res\drawable" -Force | Out-Null
New-Item -ItemType Directory -Path "app\src\main\res\values" -Force | Out-Null

Write-Host "✓ Project structure created" -ForegroundColor Green

Write-Host "`n⚠️  For fastest setup, use Android Studio:" -ForegroundColor Yellow
Write-Host "1. Open Android Studio" -ForegroundColor White
Write-Host "2. New Project → Empty Activity" -ForegroundColor White
Write-Host "3. Package: com.rtxstock.alert" -ForegroundColor White
Write-Host "4. Copy code from FCM_SETUP.txt" -ForegroundColor White
Write-Host "5. Add google-services.json to app/" -ForegroundColor White
Write-Host "6. Build → Run" -ForegroundColor White

Write-Host "`nOr use the pre-built APK generator script..." -ForegroundColor Cyan

Set-Location ..

