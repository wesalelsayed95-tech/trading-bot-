import os
import json
import random
import time
from eth_account import Account

Account.enable_unaudited_hdwallet_features()

def generate_wallets(num_wallets=10):
    wallets = []
    print(f"[*] Generating {num_wallets} random EVM wallets...")
    
    for i in range(num_wallets):
        account = Account.create()
        wallet_info = {
            "id": i + 1,
            "address": account.address,
            "private_key": account._private_key.hex()
        }
        wallets.append(wallet_info)
    
    with open("wallets.json", "w") as f:
        json.dump(wallets, f, indent=4)
        
    print("[+] Wallets generated and saved in 'wallets.json'!")
    return wallets

def simulate_human_farming():
    if not os.path.exists("wallets.json"):
        print("[-] Error: wallets.json not found.")
        return

    with open("wallets.json", "r") as f:
        wallets = json.load(f)

    print(f"[*] Starting farming simulation for {len(wallets)} wallets...")

    for wallet in wallets:
        print(f"\n--- Processing Wallet #{wallet['id']} ({wallet['address'][:6]}...{wallet['address'][-4:]}) ---")
        
        delay = random.randint(30, 120)
        print(f"[*] Anti-Sybil: Sleeping for {delay} seconds...")
        time.sleep(delay)
        
        random_amount = round(random.uniform(0.0001, 0.005), 6)
        print(f"[*] Simulating transaction with amount: {random_amount} ETH...")
        
        print(f"[+] Wallet #{wallet['id']} action successful.")

    print("\n[+] Cycle completed successfully.")

if __name__ == "__main__":
    if not os.path.exists("wallets.json"):
        generate_wallets(20)
    
    simulate_human_farming()
