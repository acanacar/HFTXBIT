import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

trade_data = pd.read_csv(fr'C:\Users\a.acar\PycharmProjects\HFTCBT\trade_data\20190104.csv', sep=',')
trade_data['timestamp'] = trade_data.timestamp.str.replace('D', ' ')
trade_data['timestamp'] = pd.to_datetime(trade_data['timestamp'], unit='ns')
trade_data.set_index(['timestamp', 'symbol'], inplace=True)
trade_data.sort_index(inplace=True)
trade_data.sort_values(['timestamp', 'symbol'], inplace=True)
# symbols = list(trade_data.symbol.unique())
# trade_data['timestamp_temp'] = trade_data['timestamp'].copy()
# th=100
# i=0
# sub_th=10
# k=0
# while i<th:
#     print(i)
#     if (trade_data.timestamp.value_counts() != 1).sum()>0:
#         if k>sub_th:
#             k=0
#             print((trade_data.timestamp.value_counts() != 1).sum())
#         trade_data['diff_1_period_as_ns'] = trade_data['timestamp'].diff()
#         print(trade_data.head())
#         trade_data.loc[trade_data['diff_1_period_as_ns'],'timestamp']=trade_data.loc[trade_data['diff_1_period_as_ns']==0,'timestamp']+pd.Timedelta(nanoseconds=1)
#
#     k+=1
#     i+=1

vol_pivot = trade_data.pivot(index=['timestamp', 'trdMatchID'], columns='symbol', values=['foreignNotional'])
price_pivot = trade_data.pivot(index=['timestamp', 'trdMatchID'], columns='symbol', values=['price'])
price_pivot.ffill(inplace=True)
price_pivot.bfill(inplace=True)
price_pivot = price_pivot.droplevel(level=0, axis=1)
xbt = price_pivot[['XBTUSD']]
indice_A_components = ['ADAH19', 'BCHH19', 'EOSH19', 'ETHH19', 'ETHUSD', 'LTCH19', 'TRXH19']
indice_A = price_pivot[indice_A_components].mean(axis=1)
indice_B = price_pivot.drop('XBTUSD', axis=1).mean(axis=1)
xbt['indice'] = indice_A.values
price_data = xbt.droplevel(level=1, axis=0)
price_data['ratio'] = price_data['XBTUSD'] / price_data['indice']
price_data['seconds'] = price_data.index - price_data.index[0]
price_data['seconds'] = (price_data.index - price_data.index[0]).total_seconds()
price_data['f1'] = price_data.ratio - price_data.ratio.rolling(50).mean()
price_data['f2'] = np.sign(price_data['f1'])
price_data['direction_xbt'] = np.sign(price_data['XBTUSD'].diff(10))
price_data['future_direction_xbt'] = price_data['direction_xbt'].shift(-10)
price_data[['f2', 'future_direction_xbt']].value_counts().sort_index()

plt.rcParams["figure.figsize"] = [18, 10]
plt.rcParams["figure.autolayout"] = True

plt.rcParams["figure.dpi"] = 180

plt.close()

price_data.loc[(price_data.seconds >= 2710) & (price_data.seconds < 301500), 'ratio'].plot()
ax = price_data.loc[(price_data.seconds >= 2710) & (price_data.seconds < 301500), 'XBTUSD'].plot(secondary_y=True)
ax.set_ylabel('xbt')
plt.legend()
# price_data.loc[(price_data.seconds>=2700)&(price_data.seconds<2705),['ratio','XBTUSD']].plot(sharex=True)
plt.show()

plt.close()

price_data.loc[(price_data.seconds >= 2710) & (price_data.seconds < 301500), 'f1'].plot()
plt.show()

# trade_data_xbtusd = trade_data.loc[trade_data.symbol == 'XBTUSD'].copy()
