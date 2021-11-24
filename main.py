import os
import pandas as pd
from binance import Client
import matplotlib.pyplot as plt
import sqlalchemy
from binance import BinanceSocketManager

api_key = os.environ.get("API_KEY")
secret_key = os.environ.get("SECRET_KEY")


def getMinuteData(symbol, interval, lookback):
    frame = pd.DataFrame(client.get_historical_klines(symbol, interval, lookback + " min ago UTC-05:00"))
    frame = frame.iloc[:, :6]
    frame.columns = ["Time", "Open", "High", "Low", "Close", "Volume"]
    frame = frame.set_index("Time")
    frame.index = pd.to_datetime(frame.index, unit="ms")
    frame = frame.astype(float)
    return frame


def strategyTest(symbol, qty, entered=False):
    df = getMinuteData(symbol, '1m', '30')
    cumulret = (df.Open.pct_change() + 1).cumprod() - 1
    if not entered:
        if cumulret[-1] < -0.002:
            order = client.create_order(symbol=symbol, side="BUY", type="MARKET", quantity=qty)
            print(order)
            entered = True
        else:
            print("No Trade Executed.")
    if entered:
        """Condition for selling here"""


if __name__ == '__main__':
    client = Client(api_key=api_key, api_secret=secret_key)
    client_account = client.get_account()
    btc_history = getMinuteData('BTCUSDT', '1m', '30')
    # plt.plot(btc_history)
    # plt.show()