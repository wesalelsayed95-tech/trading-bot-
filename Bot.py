import asyncio
import httpx
from datetime import datetime, timezone

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
        
        # تنفيذ الإشارة أو الطباعة المباشرة بدون روابط
        print(f"[{now}] Trade Signal Generated Successfully: {signal_data}")
        
        trade_executed_today = True

if __name__ == "__main__":
    asyncio.run(execute_trade())
