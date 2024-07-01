import requests
import json
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
#import qgrid
import time


def get_bybit_bars(symbol, interval, startTime, endTime):
    url = "https://api.bybit.com/v2/public/kline/list"

    startTime = str(int(startTime.timestamp()))
    endTime = str(int(endTime.timestamp()))

    req_params = {"symbol": symbol, 'interval': interval, 'from': startTime, 'to': endTime}

    df = pd.DataFrame(json.loads(requests.get(url, params=req_params).text)['result'])

    if (len(df.index) == 0):
        return None

    df.index = [dt.datetime.fromtimestamp(x) for x in df.open_time]

    return df

if __name__ == "__main__":
    df = get_bybit_bars('.MBTCUSD', 5, dt.datetime(2022, 4, 20), dt.datetime(2022, 4, 25))
    print(df)
