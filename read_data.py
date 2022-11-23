import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

trade_data = pd.read_csv(fr'C:\Users\a.acar\PycharmProjects\HFTCBT\trade_data\20190104.csv', sep=',')
trade_data_xbtusd = trade_data.loc[trade_data.symbol == 'XBTUSD'].copy()

quote_data = pd.read_csv(fr'C:\Users\a.acar\PycharmProjects\HFTCBT\quote_data\20190104.csv', sep=',')
quote_data_xbtusd = quote_data.loc[quote_data.symbol == 'XBTUSD'].copy()

N = 150000
xx = trade_data_xbtusd.head(N)
xx['timestamp'] = xx.timestamp.str.replace('D', ' ')
xx['timestamp'] = pd.to_datetime(xx['timestamp'], unit='ns')

yy = quote_data_xbtusd.head(N)
yy['timestamp'] = yy.timestamp.str.replace('D', ' ')
yy['timestamp'] = pd.to_datetime(yy['timestamp'], unit='ns')

xx['msg_type'] = 'E'
zz = pd.merge(yy, xx, 'left', on='timestamp', suffixes=('', '_y'))
zz.drop(axis=1, labels=['symbol_y'], inplace=True)

zz['mid_price'] = (zz['bidPrice'] + zz['askPrice']) / 2
zz['active_level_size'] = zz['askSize'] + zz['bidSize']
zz['micro_price'] = (zz['bidPrice'] * zz['askSize'] + zz['askPrice'] * zz['bidSize']) / (zz['active_level_size'])
zz['spread'] = zz['askPrice'] - zz['bidPrice']
zz['imb_size'] = (zz['bidSize'] - zz['askSize']) / (zz['bidSize'] + zz['askSize'])
zz['previous_imb_size'] = zz['imb_size'].shift(1)

(zz['micro_price'] - zz['mid_price']).plot()
zz['spread'].plot()
zz['imb_size'].plot()

plt.hist(zz['imb_size'], bins=np.linspace(-1, 1, num=50))
plt.title("Hist of imbalance")
plt.xlabel(r'$\rho$')
plt.ylabel('Freq')
plt.show()

trades = pd.read_csv('https://raw.githubusercontent.com/ASXPortfolio/jupyter-notebooks-data/main/CBA_trades.csv')
trades.head()

