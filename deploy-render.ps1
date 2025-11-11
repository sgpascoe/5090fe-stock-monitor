# Deploy RTX 5090 Stock Monitor to Render using PowerShell and Render API
# Requires: Render API Key (get from https://dashboard.render.com/account/api-keys)

param(
    [Parameter(Mandatory=$true)]
    [string]$ApiKey,
    
    [string]$ServiceName = "nvidia-stock-monitor",
    [string]$RepoUrl = "https://github.com/CoveMarketing/5090fe-stock-monitor",
    [string]$Branch = "master"
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Render API base URL
$baseUrl = "https://api.render.com/v1"

# Headers with API key
$headers = @{
    "Authorization" = "Bearer $ApiKey"
    "Accept" = "application/json"
    "Content-Type" = "application/json"
}

Write-Host "🚀 Deploying RTX 5090 Stock Monitor to Render..." -ForegroundColor Cyan

try {
    # Get owner ID (your account)
    Write-Host "`n📋 Getting account information..." -ForegroundColor Yellow
    $owner = Invoke-RestMethod -Uri "$baseUrl/owners" -Headers $headers -Method Get
    $ownerId = $owner[0].owner.id
    Write-Host "✓ Account ID: $ownerId" -ForegroundColor Green
    
    # Create background worker service
    Write-Host "`n🔧 Creating background worker service..." -ForegroundColor Yellow
    
    $serviceBody = @{
        type = "worker"
        name = $ServiceName
        ownerId = $ownerId
        repo = $RepoUrl
        branch = $Branch
        runtime = "python"
        buildCommand = "pip install -r requirements.txt"
        startCommand = "python nvidia_stock_monitor.py"
        planId = "free"  # Free tier
        envVars = @(
            @{
                key = "CHECK_INTERVAL"
                value = "30"
            }
        )
    } | ConvertTo-Json -Depth 10
    
    $service = Invoke-RestMethod -Uri "$baseUrl/services" -Headers $headers -Method Post -Body $serviceBody
    Write-Host "✓ Service created successfully!" -ForegroundColor Green
    Write-Host "  Service ID: $($service.service.id)" -ForegroundColor Gray
    Write-Host "  Service URL: https://dashboard.render.com/web/$($service.service.id)" -ForegroundColor Gray
    
    Write-Host "`n✅ Deployment initiated!" -ForegroundColor Green
    Write-Host "`n📝 Next steps:" -ForegroundColor Cyan
    Write-Host "1. Go to: https://dashboard.render.com/web/$($service.service.id)" -ForegroundColor White
    Write-Host "2. Add environment variables for notifications:" -ForegroundColor White
    Write-Host "   - DISCORD_WEBHOOK (recommended - easiest)" -ForegroundColor Gray
    Write-Host "   - Or TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID" -ForegroundColor Gray
    Write-Host "   - Or PUSHOVER_TOKEN + PUSHOVER_USER" -ForegroundColor Gray
    Write-Host "3. The service will start automatically!" -ForegroundColor White
    
} catch {
    Write-Host "`n❌ Error: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        Write-Host "Details: $($_.ErrorDetails.Message)" -ForegroundColor Yellow
    }
    Write-Host "`n💡 Tip: Get your API key from: https://dashboard.render.com/account/api-keys" -ForegroundColor Cyan
    exit 1
}

