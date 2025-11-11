# Quick FCM Test Script
# Tests FCM notification sending

param(
    [string]$ServerKey = $env:FCM_SERVER_KEY,
    [string]$DeviceToken = $env:FCM_DEVICE_TOKEN,
    [string]$Message = "Test alert from RTX Stock Monitor"
)

if (-not $ServerKey -or -not $DeviceToken) {
    Write-Host "❌ FCM credentials not set!" -ForegroundColor Red
    Write-Host "Set FCM_SERVER_KEY and FCM_DEVICE_TOKEN environment variables" -ForegroundColor Yellow
    Write-Host "Or pass them as parameters:" -ForegroundColor Yellow
    Write-Host "  .\test-fcm.ps1 -ServerKey 'YOUR_KEY' -DeviceToken 'YOUR_TOKEN'" -ForegroundColor Cyan
    exit 1
}

Write-Host "🧪 Testing FCM notification..." -ForegroundColor Cyan
Write-Host "Server Key: $($ServerKey.Substring(0, 20))..." -ForegroundColor Gray
Write-Host "Device Token: $($DeviceToken.Substring(0, 20))..." -ForegroundColor Gray
Write-Host ""

$headers = @{
    "Authorization" = "key=$ServerKey"
    "Content-Type" = "application/json"
}

$body = @{
    to = $DeviceToken
    priority = "high"
    notification = @{
        title = "🚨 RTX 5090 Test Alert"
        body = $Message
        sound = "default"
        channel_id = "high_priority_alerts"
    }
    data = @{
        click_action = "OPEN_NVIDIA_STORE"
        url = "https://www.nvidia.com/en-gb/shop/"
    }
    android = @{
        priority = "high"
        notification = @{
            channel_id = "high_priority_alerts"
            sound = "default"
            priority = "high"
        }
    }
} | ConvertTo-Json -Depth 10

try {
    $response = Invoke-RestMethod -Uri "https://fcm.googleapis.com/fcm/send" -Method Post -Headers $headers -Body $body
    
    if ($response.success -eq 1) {
        Write-Host "✅ FCM notification sent successfully!" -ForegroundColor Green
        Write-Host "Check your Android device for the notification." -ForegroundColor Cyan
    } else {
        Write-Host "⚠️  Response: $($response | ConvertTo-Json)" -ForegroundColor Yellow
    }
} catch {
    Write-Host "❌ Error sending FCM notification:" -ForegroundColor Red
    Write-Host $_.Exception.Message -ForegroundColor Red
    if ($_.ErrorDetails.Message) {
        Write-Host $_.ErrorDetails.Message -ForegroundColor Yellow
    }
}

