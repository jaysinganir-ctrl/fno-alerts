import requests
import pandas as pd
import yfinance as yf
from datetime import datetime

TOKEN = "8956026871:AAEAzvBeHNDQ4Gi1z_AsRreZmfw5W2l90RU"
CHAT_ID = "729532479"

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    params = {"chat_id": CHAT_ID, "text": text}
    requests.get(url, params=params)

def get_top_stocks():
    stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS", "ICICIBANK.NS", "SBIN.NS"]

    data_list = []
    for symbol in stocks:
        data = yf.download(symbol, period="1d", interval="1d")
        if not data.empty:
            close = data["Close"].values[-1].item()   # convert to float
            open_price = data["Open"].values[-1].item()
            change_pct = ((close - open_price) / open_price) * 100
            data_list.append((symbol, close, change_pct))

    df = pd.DataFrame(data_list, columns=["Stock", "Price", "Change%"])
    top_gainers = df.sort_values("Change%", ascending=False).head(5)
    top_losers = df.sort_values("Change%").head(5)

    report = "📈 Top Gainers:\n"
    for _, row in top_gainers.iterrows():
        report += f"{row['Stock']}: {row['Price']:.2f} ({row['Change%']:.2f}%)\n"

    report += "\n📉 Top Losers:\n"
    for _, row in top_losers.iterrows():
        report += f"{row['Stock']}: {row['Price']:.2f} ({row['Change%']:.2f}%)\n"

    return report

if __name__ == "__main__":
    now = datetime.now().strftime("%d-%m-%Y %H:%M")
    message = f"📊 F&O Stock Update ({now})\n\n{get_top_stocks()}"
    send_message(message)
