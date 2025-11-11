# Run Stock Monitor Locally
# ==========================
# Run this to monitor continuously with 15-30 second checks

# Set your Pushover credentials (or use environment variables)
$env:PUSHOVER_USER = "uevm87p2unp2x3b7yi1nsgm7xj2w4g"
$env:PUSHOVER_TOKEN = "afwtah7mztb9nb4nd2fvtr2i8fuwqc"

# Set check interval (15-30 seconds)
$env:CHECK_INTERVAL = "20"  # Change to 15, 20, 25, or 30 as needed
$env:BACKOFF_DELAY = "5"

# Run the monitor
python nvidia_stock_monitor.py

# The script will:
# - Check every 20 seconds (or whatever CHECK_INTERVAL you set)
# - Send alerts when stock is detected
# - Send small alerts on errors/backoffs
# - Run continuously until you stop it (Ctrl+C)

