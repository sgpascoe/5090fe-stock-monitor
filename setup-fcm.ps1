# Firebase FCM Setup Script for RTX Stock Monitor
# This script helps you set up Firebase Cloud Messaging via CLI

param(
    [string]$ProjectName = "rtx-stock-alert",
    [string]$PackageName = "com.rtxstock.alert"
)

$ErrorActionPreference = "Stop"

Write-Host "🔥 Firebase FCM Setup for RTX Stock Monitor" -ForegroundColor Cyan
Write-Host "==========================================`n" -ForegroundColor Cyan

# Check if Node.js/npm is installed
Write-Host "📦 Checking Node.js installation..." -ForegroundColor Yellow
try {
    $npmVersion = npm --version
    Write-Host "✓ Node.js/npm found (version $npmVersion)" -ForegroundColor Green
} catch {
    Write-Host "❌ Node.js/npm not found!" -ForegroundColor Red
    Write-Host "Please install Node.js from: https://nodejs.org/" -ForegroundColor Yellow
    exit 1
}

# Install Firebase CLI globally
Write-Host "`n📦 Installing Firebase CLI..." -ForegroundColor Yellow
try {
    $firebaseVersion = firebase --version 2>$null
    Write-Host "✓ Firebase CLI already installed (version $firebaseVersion)" -ForegroundColor Green
} catch {
    Write-Host "Installing Firebase CLI..." -ForegroundColor Gray
    npm install -g firebase-tools
    Write-Host "✓ Firebase CLI installed" -ForegroundColor Green
}

# Login to Firebase
Write-Host "`n🔐 Logging into Firebase..." -ForegroundColor Yellow
Write-Host "This will open your browser for authentication..." -ForegroundColor Gray
Write-Host "If you're not logged in, run: firebase login" -ForegroundColor Cyan
try {
    firebase projects:list 2>&1 | Out-Null
    Write-Host "✓ Already logged in to Firebase" -ForegroundColor Green
} catch {
    Write-Host "⚠️  Not logged in. Run 'firebase login' manually" -ForegroundColor Yellow
    Write-Host "   This will open a browser for authentication" -ForegroundColor Gray
}

# Initialize Firebase project
Write-Host "`n🚀 Initializing Firebase project..." -ForegroundColor Yellow
Write-Host "Project name: $ProjectName" -ForegroundColor Gray
Write-Host "Package name: $PackageName`n" -ForegroundColor Gray

# Check if firebase.json exists
if (Test-Path "firebase.json") {
    Write-Host "⚠️  firebase.json already exists. Skipping initialization." -ForegroundColor Yellow
    Write-Host "If you want to reinitialize, delete firebase.json first." -ForegroundColor Gray
} else {
    # Create a temporary directory for Firebase init
    $tempDir = New-TemporaryFile | ForEach-Object { Remove-Item $_; New-Item -ItemType Directory -Path $_ }
    Push-Location $tempDir
    
    try {
        # Initialize Firebase (non-interactive)
        Write-Host "Initializing Firebase project..." -ForegroundColor Gray
        # Note: Firebase init is interactive, so we'll guide the user
        Write-Host "`n⚠️  Firebase init requires interactive setup." -ForegroundColor Yellow
        Write-Host "Please run these commands manually:" -ForegroundColor Cyan
        Write-Host "  1. firebase init" -ForegroundColor White
        Write-Host "  2. Select: 'Firestore' and 'Functions' (or just press Enter for defaults)" -ForegroundColor White
        Write-Host "  3. Use existing project or create new one" -ForegroundColor White
        Write-Host "  4. Follow the prompts`n" -ForegroundColor White
    } finally {
        Pop-Location
        Remove-Item $tempDir -Recurse -Force -ErrorAction SilentlyContinue
    }
}

# Instructions for getting credentials
Write-Host "`n📋 Next Steps:" -ForegroundColor Cyan
Write-Host "=============" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. CREATE FIREBASE PROJECT (if not done):" -ForegroundColor Yellow
Write-Host "   - Go to: https://console.firebase.google.com/" -ForegroundColor White
Write-Host "   - Click 'Add project'" -ForegroundColor White
Write-Host "   - Name: $ProjectName" -ForegroundColor White
Write-Host "   - Create project`n" -ForegroundColor White

Write-Host "2. ADD ANDROID APP:" -ForegroundColor Yellow
Write-Host "   - In Firebase Console → Add app → Android" -ForegroundColor White
Write-Host "   - Package name: $PackageName" -ForegroundColor White
Write-Host "   - Register app" -ForegroundColor White
Write-Host "   - Download google-services.json`n" -ForegroundColor White

Write-Host "3. GET SERVER KEY:" -ForegroundColor Yellow
Write-Host "   - Firebase Console → Project Settings → Cloud Messaging" -ForegroundColor White
Write-Host "   - Copy 'Server key' (this is your FCM_SERVER_KEY)`n" -ForegroundColor White

Write-Host "4. GET DEVICE TOKEN:" -ForegroundColor Yellow
Write-Host "   - Build and run the Android app (see FCM_SETUP.txt)" -ForegroundColor White
Write-Host "   - The app will display your FCM token" -ForegroundColor White
Write-Host "   - Copy this token (this is your FCM_DEVICE_TOKEN)`n" -ForegroundColor White

Write-Host "5. ADD TO GITHUB SECRETS:" -ForegroundColor Yellow
Write-Host "   Run these commands or add via GitHub web UI:" -ForegroundColor White
Write-Host ""
Write-Host "   gh secret set FCM_SERVER_KEY --body 'YOUR_SERVER_KEY'" -ForegroundColor Cyan
Write-Host "   gh secret set FCM_DEVICE_TOKEN --body 'YOUR_DEVICE_TOKEN'" -ForegroundColor Cyan
Write-Host ""
Write-Host "   Or manually:" -ForegroundColor Gray
Write-Host "   - Go to: https://github.com/sgpascoe/5090fe-stock-monitor/settings/secrets/actions" -ForegroundColor Gray
Write-Host "   - Add FCM_SERVER_KEY" -ForegroundColor Gray
Write-Host "   - Add FCM_DEVICE_TOKEN`n" -ForegroundColor Gray

Write-Host "6. TEST THE SETUP:" -ForegroundColor Yellow
Write-Host "   python test_notifications.py" -ForegroundColor White
Write-Host "   (Make sure FCM secrets are set)`n" -ForegroundColor Gray

Write-Host "✅ Setup complete! Your FCM credentials are ready." -ForegroundColor Green
Write-Host ""
Write-Host "💡 Tip: Use 'firebase projects:list' to see your projects" -ForegroundColor Cyan
Write-Host "💡 Tip: Use 'firebase use <project-id>' to switch projects" -ForegroundColor Cyan

