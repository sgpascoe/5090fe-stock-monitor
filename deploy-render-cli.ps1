# Deploy RTX 5090 Stock Monitor to Render using PowerShell and Render API
# Usage: .\deploy-render-cli.ps1
# Or set RENDER_API_KEY environment variable

param(
    [string]$ApiKey = $env:RENDER_API_KEY,
    [string]$ServiceName = "nvidia-stock-monitor",
    [string]$RepoUrl = "https://github.com/sgpascoe/5090fe-stock-monitor",
    [string]$Branch = "master"
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Get API key if not provided
if (-not $ApiKey) {
    Write-Host "Render API Key required!" -ForegroundColor Yellow
    Write-Host "Get it from: https://dashboard.render.com/account/api-keys" -ForegroundColor Cyan
    $ApiKey = Read-Host "Enter your Render API Key"
}

if (-not $ApiKey) {
    Write-Host "API Key is required!" -ForegroundColor Red
    exit 1
}

# Render API base URL
$baseUrl = "https://api.render.com/v1"

# Headers with API key
$headers = @{
    "Authorization" = "Bearer $ApiKey"
    "Accept" = "application/json"
    "Content-Type" = "application/json"
}

Write-Host "Deploying RTX 5090 Stock Monitor to Render..." -ForegroundColor Cyan
Write-Host "Repository: $RepoUrl" -ForegroundColor Gray
Write-Host "Branch: $Branch" -ForegroundColor Gray

try {
    # Get owner ID (your account)
    Write-Host "`nGetting account information..." -ForegroundColor Yellow
    $ownerResponse = Invoke-RestMethod -Uri "$baseUrl/owners" -Headers $headers -Method Get
    $ownerId = $ownerResponse[0].owner.id
    Write-Host "Account ID: $ownerId" -ForegroundColor Green
    
    # Create background worker service
    Write-Host "`nCreating background worker service..." -ForegroundColor Yellow
    
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
                value = "15"
            }
        )
    } | ConvertTo-Json -Depth 10
    
    Write-Host "Sending request to Render API..." -ForegroundColor Gray
    $service = Invoke-RestMethod -Uri "$baseUrl/services" -Headers $headers -Method Post -Body $serviceBody
    Write-Host "Service created successfully!" -ForegroundColor Green
    Write-Host "  Service ID: $($service.service.id)" -ForegroundColor Gray
    Write-Host "  Service URL: https://dashboard.render.com/web/$($service.service.id)" -ForegroundColor Cyan
    
    Write-Host "`nDeployment initiated!" -ForegroundColor Green
    Write-Host "`nNext steps:" -ForegroundColor Cyan
    Write-Host "1. Go to: https://dashboard.render.com/web/$($service.service.id)" -ForegroundColor White
    Write-Host "2. Add environment variables for notifications:" -ForegroundColor White
    Write-Host "   - DISCORD_WEBHOOK (recommended - easiest)" -ForegroundColor Gray
    Write-Host "   - Or TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID" -ForegroundColor Gray
    Write-Host "   - Or PUSHOVER_TOKEN + PUSHOVER_USER" -ForegroundColor Gray
    Write-Host "3. The service will start automatically!" -ForegroundColor White
    
} catch {
    Write-Host "`nError: $($_.Exception.Message)" -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        $errorDetails = $_.ErrorDetails.Message | ConvertFrom-Json -ErrorAction SilentlyContinue
        if ($errorDetails) {
            Write-Host "Details: $($errorDetails.message)" -ForegroundColor Yellow
        } else {
            Write-Host "Details: $($_.ErrorDetails.Message)" -ForegroundColor Yellow
        }
    }
    Write-Host "`nTip: Get your API key from: https://dashboard.render.com/account/api-keys" -ForegroundColor Cyan
    exit 1
}
