import asyncio
import websockets
import json
import requests

# Helius WebSocket and API Endpoints
API_KEY = "YOUR_API_KEY"
WS_URL = f"wss://mainnet.helius-rpc.com/?api-key={API_KEY}"
PARSE_TX_URL = f"https://api.helius.xyz/v0/transactions/?api-key={API_KEY}"

# Wallet to track
TRACKED_WALLET = "CkgRjE5ZoQe7tNC6DpWpxg8DfN4muZEPJ9yYbWjAwwt8"  # Replace with actual wallet address

async def handle_transaction(tx_signature):
    """Fetch and parse transaction details."""
    response = requests.post(PARSE_TX_URL, json={"transactions": [tx_signature]})
    if response.status_code == 200:
        tx_data = response.json()[0]
        status = tx_data.get("meta", {}).get("err", None)
        
        if status is None:
            print(f"✅ Transaction Confirmed: {tx_signature}")
            process_transaction(tx_data)
        else:
            print(f"❌ Transaction Failed: {tx_signature}")
    else:
        print("Error fetching transaction details.")

def process_transaction(tx_data):
    """Analyze transaction type (buy/sell/swap) and extract relevant info."""
    instructions = tx_data.get("transaction", {}).get("message", {}).get("instructions", [])
    pre_balances = tx_data.get("meta", {}).get("preTokenBalances", [])
    post_balances = tx_data.get("meta", {}).get("postTokenBalances", [])
    
    for instr in instructions:
        program = instr.get("program")
        if program == "spl-token":
            source = instr.get("source")
            destination = instr.get("destination")
            amount = instr.get("amount")
            mint = instr.get("mint")
            print(f"🔄 Token Transfer: {amount} of {mint} from {source} to {destination}")
        elif program == "swap":
            print("🔁 Swap detected!")
            analyze_swap(pre_balances, post_balances)

def analyze_swap(pre_balances, post_balances):
    """Identify what token was bought and sold."""
    for pre, post in zip(pre_balances, post_balances):
        if pre["owner"] == TRACKED_WALLET and post["owner"] == TRACKED_WALLET:
            change = float(post["uiTokenAmount"]["amount"]) - float(pre["uiTokenAmount"]["amount"]) 
            mint = post["mint"]
            if change > 0:
                print(f"🟢 Bought {change} of {mint}")
            elif change < 0:
                print(f"🔴 Sold {abs(change)} of {mint}")

async def subscribe_to_transactions():
    """Connects to WebSocket and listens for tracked wallet transactions."""
    while True:
        try:
            async with websockets.connect(WS_URL) as ws:
                print("✅ Connected to WebSocket")
                
                # Subscribe to the wallet's transactions
                await ws.send(json.dumps({
                    "jsonrpc": "2.0",
                    "id": 1,
                    "method": "logsSubscribe",
                    "params": [{
                        "mentions": [TRACKED_WALLET]
                    }, {
                        "commitment": "finalized"
                    }]
                }))
                
                while True:
                    try:
                        message = await ws.recv()
                        data = json.loads(message)
                        tx_signature = data.get("params", {}).get("result", {}).get("value", {}).get("signature")
                        if tx_signature:
                            print(f"🔔 New Transaction Detected: {tx_signature}")
                            await handle_transaction(tx_signature)
                    except Exception as e:
                        print(f"Error: {e}")
                        break
        except Exception as e:
            print(f"WebSocket connection error: {e}")
            await asyncio.sleep(5)  # Wait before reconnecting

asyncio.run(subscribe_to_transactions())
