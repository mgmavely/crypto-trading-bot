import os
import asyncio
import pandas as pd
import sqlalchemy
from binance import BinanceSocketManager, AsyncClient

api_key = os.environ.get("API_KEY")
secret_key = os.environ.get("SECRET_KEY")


async def main():
    client = await AsyncClient.create(api_key=api_key, api_secret=secret_key)
    bsm = BinanceSocketManager(client)
    socket = bsm.trade_socket('BTCUSDT')
    async with socket as tscm:
        while True:
            res = await tscm.recv()
            df = createDF(res)
            df.to_sql('BTCUSDT', engine, if_exists='append', index=False)
            print(df)

    await client.close_connection()


def createDF(msg):
    df = pd.DataFrame([msg])
    df = df.loc[:, ['s', 'E', 'p']]
    df.columns = ['Symbol', 'Time', 'Price']
    df.Price = df.Price.astype(float)
    df.Time = pd.to_datetime(df.Time, unit='ms')
    return df


if __name__ == '__main__':
    engine = sqlalchemy.create_engine('sqlite:///BTCUSDTstream.db')
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
