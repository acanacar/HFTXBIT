'''
gunluk saatlere gore hacim oranlari nasil degisiyor
'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
pd.options.display.float_format = "{:,.2f}".format
from helpers import plot_daily_volume_by_month

daily_trade_datas = []
files_dir = Path(fr'C:\Users\a.acar\PycharmProjects\HFTCBT\trade_data\daily')
for file in files_dir.iterdir():
    print(fr'reading {file.name}')
    trade_data = pd.read_csv(file)
    trade_data_xbtusd = trade_data.loc[trade_data.symbol == 'XBTUSD'].copy()
    daily_trade_datas.append(trade_data_xbtusd)

data_xbtusd = pd.concat(daily_trade_datas,axis=0)
data_xbtusd.to_pickle(fr'C:\Users\a.acar\PycharmProjects\HFTCBT\trade_data\xbtusd_20190101_20190528.pkl')
data_xbtusd['timestamp'] = data_xbtusd.timestamp.str.replace('D', ' ')
data_xbtusd['timestamp'] = pd.to_datetime(data_xbtusd['timestamp'], unit='ns')
data_xbtusd['volume'] = data_xbtusd['size'] / data_xbtusd['price']

data_xbtusd_processed = data_xbtusd.groupby('timestamp').agg(
    side=('side', 'last'),
    volume=('volume', 'sum'),
    size=('size', 'sum'),
    homeNotional=('homeNotional', 'sum'),
    tickDirection=('tickDirection', 'last')
)
data_xbtusd_processed['day'] = data_xbtusd_processed.index.floor('D')
data_xbtusd_processed['intraday_time_h'] = data_xbtusd_processed.index.strftime("%H")
data_xbtusd_processed['month'] = data_xbtusd_processed.index.strftime('%Y-%m')

data_xbtusd_processed.to_pickle(fr'C:\Users\a.acar\PycharmProjects\HFTCBT\trade_data\xbtusd_20190101_20190528_processed.pkl')
