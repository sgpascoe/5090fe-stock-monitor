#!/usr/bin/env python3
"""
Deploy RTX 5090 Stock Monitor to Render using Render API
Run: render login first to authenticate, then run this script
"""

import subprocess
import json
import os

def run_render_command(cmd):
    """Run a render CLI command"""
    try:
        result = subprocess.run(
            ["render",] + cmd.split(),
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.stderr}")
        return None
    except FileNotFoundError:
        print("Render CLI not found. Installing...")
        subprocess.run(["pip", "install", "--user", "render-cli"], check=True)
        print("Please run 'render login' first, then run this script again.")
        return None

def deploy_to_render():
    """Deploy the background worker to Render"""
    print("Deploying RTX 5090 Stock Monitor to Render...")
    
    # Check if authenticated
    auth_check = run_render_command("whoami")
    if not auth_check:
        print("\n⚠️  Not authenticated. Please run:")
        print("   render login")
        print("\nThen run this script again.")
        return
    
    print(f"✓ Authenticated as: {auth_check}")
    
    # Create service using render.yaml
    print("\nCreating background worker service...")
    result = run_render_command("services create --file render.yaml")
    
    if result:
        print(f"✓ Service created successfully!")
        print(f"\n{result}")
        print("\n📝 Next steps:")
        print("1. Go to https://dashboard.render.com")
        print("2. Find your service 'nvidia-stock-monitor'")
        print("3. Add environment variables for notifications:")
        print("   - DISCORD_WEBHOOK (recommended)")
        print("   - Or TELEGRAM_BOT_TOKEN + TELEGRAM_CHAT_ID")
        print("   - Or PUSHOVER_TOKEN + PUSHOVER_USER")
        print("4. The service will start automatically!")
    else:
        print("\n⚠️  Service creation failed. You may need to:")
        print("1. Run 'render login' to authenticate")
        print("2. Or create the service manually at https://dashboard.render.com")

if __name__ == "__main__":
    deploy_to_render()

