import requests
import time
from keep_alive import keep_alive

# Telegram bot token and private channel chat ID
BOT_TOKEN = "YOUR_BOT_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

WATCHLIST = {
    "bitcoin": 50000,
    "solana": 80,
    "pepe": 0.000001
}

def get_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    try:
        response = requests.get(url)
        return response.json()[coin_id]["usd"]
    except:
        return None

def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=payload)

def main():
    print("Crypto bot running...")
    send_alert("✅ CryptoDipAlerts VIP bot is now active.")
    while True:
        for coin, target in WATCHLIST.items():
            price = get_price(coin)
            if price is not None and price <= target:
                send_alert(f"🚨 {coin.upper()} dropped to ${price} (target: ${target})")
        time.sleep(300)

keep_alive()
main()
