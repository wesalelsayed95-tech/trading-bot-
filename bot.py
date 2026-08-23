import json
import random
import time
from web3 import Web3

RPC_LIST = [
    "https://eth-sepolia.g.alchemy.com/v2/demo",
    "https://sepolia.infura.io/v3/9aa3d95b3bc440fa88ea12eaa4456161",
    "https://rpc.ankr.com/eth_sepolia",
    "https://ethereum-sepolia-rpc.publicnode.com"
]

def get_working_w3():
    for rpc in RPC_LIST:
        w3 = Web3(Web3.HTTPProvider(rpc))
        if w3.is_connected():
            return w3
    return None

def load_wallets():
    try:
        with open("wallets.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return []

def main():
    w3 = get_working_w3()
    if not w3 or not w3.is_connected():
        return

    wallets = load_wallets()
    if not wallets:
        return

    for i, wallet in enumerate(wallets):
        address = wallet["address"]
        private_key = wallet["private_key"]
        
        try:
            balance = w3.eth.get_balance(address)
            
            if balance > 0:
                nonce = w3.eth.get_transaction_count(address)
                gas_price = w3.eth.gas_price
                
                tx = {
                    'nonce': nonce,
                    'to': address,
                    'value': w3.to_wei(0.00001, 'ether'),
                    'gas': 21000,
                    'gasPrice': gas_price,
                    'chainId': 11155111
                }
                
                signed_tx = w3.eth.account.sign_transaction(tx, private_key)
                tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
        except Exception as e:
            pass

        sleep_time = random.randint(10, 30)
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()
