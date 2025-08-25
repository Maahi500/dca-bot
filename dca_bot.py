import ccxt
import schedule
import time
import os
from dotenv import load_dotenv

# Load API keys from .env file
load_dotenv()
api_key = os.getenv('BYBIT_API_KEY')
api_secret = os.getenv('BYBIT_API_SECRET')

# Connect to Bybit testnet
exchange = ccxt.bybit({
    'apiKey': api_key,
    'secret': api_secret,
    'enableRateLimit': True,
    'testnet': True
})

# Function to buy $10 of Bitcoin
def buy_bitcoin():
    try:
        symbol = 'BTC/USDT'
        amount_usdt = 10  # $10 per purchase
        ticker = exchange.fetch_ticker(symbol)
        price = ticker['last']
        amount_btc = amount_usdt / price
        order = exchange.create_market_buy_order(symbol, amount_btc)
        print(f"Bought {amount_btc:.6f} BTC at ${price:.2f} on {time.ctime()}")
    except Exception as e:
        print(f"Error: {e}")

# Schedule to run every day at 9 AM
schedule.every().day.at("09:00").do(buy_bitcoin)

# Keep the bot running
print("DCA Bot started. Waiting for scheduled buys...")
while True:
    schedule.run_pending()
    time.sleep(60)  # Check every minute
    