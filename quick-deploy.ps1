# Quick Deploy Script for RTX 5090 Stock Monitor
# This script helps you deploy to Render via API

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "RTX 5090 Stock Monitor - Render Deploy" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if API key is provided
$apiKey = $env:RENDER_API_KEY
if (-not $apiKey) {
    Write-Host "⚠️  RENDER_API_KEY environment variable not set." -ForegroundColor Yellow
    Write-Host ""
    Write-Host "To get your API key:" -ForegroundColor White
    Write-Host "1. Go to: https://dashboard.render.com/account/api-keys" -ForegroundColor Gray
    Write-Host "2. Sign in with GitHub" -ForegroundColor Gray
    Write-Host "3. Create a new API key" -ForegroundColor Gray
    Write-Host "4. Run: `$env:RENDER_API_KEY = 'your-key-here'" -ForegroundColor Gray
    Write-Host "5. Then run this script again" -ForegroundColor Gray
    Write-Host ""
    Write-Host "OR use the web interface (easier):" -ForegroundColor Cyan
    Write-Host "1. Go to: https://dashboard.render.com" -ForegroundColor White
    Write-Host "2. Click 'New +' → 'Background Worker'" -ForegroundColor White
    Write-Host "3. Connect repo: sgpascoe/5090fe-stock-monitor" -ForegroundColor White
    Write-Host "4. Render auto-detects settings from render.yaml" -ForegroundColor White
    Write-Host "5. Add environment variables and deploy!" -ForegroundColor White
    exit 0
}

# Run deployment
Write-Host "🚀 Starting deployment..." -ForegroundColor Green
& ".\deploy-render.ps1" -ApiKey $apiKey

