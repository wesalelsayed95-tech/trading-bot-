import asyncio
import httpx
from datetime import datetime, timezone

TRADING_ACCOUNTS = {
    "FTMO": "https://webhook.your-bridge-service.com/ftmo-token",
    "FundedNext": "https://webhook.your-bridge-service.com/fundednext-token"
}

MAX_DAILY_LOSS_LIMIT = 0.04
DAILY_PROFIT_TARGET = 0.02

trade_executed_today = False
last_trade_day = None

def check_daily_reset(current_utc_time):
    global trade_executed_today, last_trade_day
    current_day = current_utc_time.day
    if last_trade_day != current_day:
        trade_executed_today = False
        last_trade_day = current_day

async def send_to_broker_lightning(client, name, url, signal):
    try:
        response = await client.post(url, json=signal, timeout=3.0)
        print(f"[{name}] Executed in lightning speed - Status: {response.status_code}")
    except Exception as e:
        print(f"[{name}] Connection error: {e}")

async def execute_trade():
    global trade_executed_today
    
    now = datetime.now(timezone.utc)
    check_daily_reset(now)
    
    if trade_executed_today:
        return

    target_hour = 8
    
    if now.hour >= target_hour:
        signal_data = {
            "action": "BUY",
            "symbol": "EURUSD",
            "volume": 0.1,
            "max_loss_limit": MAX_DAILY_LOSS_LIMIT,
            "profit_target": DAILY_PROFIT_TARGET
        }
        
        async with httpx.AsyncClient(http2=True) as client:
            tasks = [
                send_to_broker_lightning(client, name, url, signal_data)
                for name, url in TRADING_ACCOUNTS.items()
            ]
            await asyncio.gather(*tasks)
            
        trade_executed_today = True

if __name__ == "__main__":
    asyncio.run(execute_trade())
