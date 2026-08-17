import asyncio
import httpx
from datetime import datetime, timezone

# --- Broker Webhooks Configuration ---
TRADING_ACCOUNTS = {
    "FTMO": "https://webhook.your-bridge-service.com/ftmo-token",
    "FundedNext": "https://webhook.your-bridge-service.com/fundednext-token"
}

# Risk and Daily Trade Settings
MAX_DAILY_LOSS_LIMIT = 0.04    # 4% Kill Switch to protect the account
DAILY_PROFIT_TARGET = 0.02     # Daily profit target percentage

trade_executed_today = False
last_trade_day = None

def check_daily_reset(current_utc_time):
    global trade_executed_today, last_trade_day
    current_day = current_utc_time.day
    if last_trade_day != current_day:
        trade_executed_today = False
        last_trade_day = current_day
        print(f"--- New Trading Day: {current_utc_time.strftime('%Y-%m-%d')} (Ready for a new daily trade) ---")

async def send_to_broker(client, name, url, signal):
    try:
        response = await client.post(url, json=signal, timeout=10.0)
        print(f"Signal sent to {name} successfully - Status: {response.status_code}")
    except Exception as e:
        print(f"Failed to connect to {name}: {e}")

async def execute_trade():
    global trade_executed_today
    
    # Get current platform/server time (UTC)
    now = datetime.now(timezone.utc)
    check_daily_reset(now)
    
    if trade_executed_today:
        print("A new trade for today has already been executed. Waiting for tomorrow.")
        return

    # Set target execution hour based on platform time (e.g., 08:00 UTC)
    target_hour = 8
    
    if now.hour >= target_hour:
        print(f"Platform time matched ({now.strftime('%H:%M:%S')} UTC). Executing today's new trade simultaneously...")
        
        signal_data = {
            "action": "BUY",
            "symbol": "EURUSD",
            "volume": 0.1,
            "max_loss_limit": MAX_DAILY_LOSS_LIMIT,
            "profit_target": DAILY_PROFIT_TARGET
        }
        
        async with httpx.AsyncClient() as client:
            tasks = [
                send_to_broker(client, name, url, signal_data)
                for name, url in TRADING_ACCOUNTS.items()
            ]
            await asyncio.gather(*tasks)
            
        # Mark that today's trade has been successfully placed
        trade_executed_today = True

if __name__ == "__main__":
    asyncio.run(execute_trade())
