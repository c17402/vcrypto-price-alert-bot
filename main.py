import requests
import time
import os
from flask import Flask, request
from threading import Thread
import threading

# Telegram Bot Config
BOT_TOKEN = "7567902028:AAEacsyfJboni5Hhm8ixcWh46q7nyI_I-YQ"
ADMIN_USER_ID = 7636096872
CHANNEL_ID = "-1002781138110"

# Crypto Watchlist
WATCHLIST = {
    "bitcoin": 66000,
    "ethereum": 3500,
    "solana": 150,
    "pepe": 0.000012,
    "dogecoin": 0.13
}

# Flask App Setup
app = Flask(__name__)

@app.route('/')
def home():
    return "✅ Crypto Dip Bot is alive!"

@app.route(f"/{BOT_TOKEN}", methods=['POST'])
def webhook():
    data = request.get_json()
    if not data:
        return "No data"

    if "message" in data:
        msg = data["message"]
        text = msg.get("text", "")
        user_id = msg["from"]["id"]

        if user_id == ADMIN_USER_ID and text.lower() == "/invite":
            send_invite(user_id)

    return "ok"

def send_invite(user_id):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/createChatInviteLink"
    payload = {
        "chat_id": CHANNEL_ID,
        "creates_join_request": False,
        "member_limit": 1
    }
    r = requests.post(url, json=payload)
    invite_link = r.json().get("result", {}).get("invite_link")
    if invite_link:
        requests.post(f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage", data={
            "chat_id": user_id,
            "text": f"🔗 Here’s your invite link:\n{invite_link}"
        })

# Crypto Price Alerts

def get_price(coin_id):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd"
    try:
        response = requests.get(url)
        return response.json()[coin_id]["usd"]
    except:
        return None

def send_alert(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHANNEL_ID,
        "text": message
    }
    requests.post(url, data=payload)

def alert_loop():
    print("✅ Crypto bot running...")
    send_alert("✅ CryptoDipAlerts VIP bot is now active.")

    while True:
        for coin, target in WATCHLIST.items():
            price = get_price(coin)
            if price is not None and price <= target:
                send_alert(f"🚨 {coin.upper()} dropped to ${price} (target: ${target})")
        time.sleep(300)  # check every 5 minutes

# Start Flask & Bot Logic

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

if __name__ == '__main__':
    keep_alive()
    threading.Thread(target=alert_loop).start()
