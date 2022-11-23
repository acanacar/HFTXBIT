'''
bu dosya bir gunkuk xbt usd tick datasinin scatter plot ile gorsellestirilerek price ile beraber bir plotunun
cizilmesi icin olusturuldu. Datayi tanimak ve likidite tick data larin birbirlerinini tetikleyip tetiklemediginin gorulmesi icin.
'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pd.options.display.float_format = "{:,.2f}".format

trade_data = pd.read_csv(fr'C:\Users\a.acar\PycharmProjects\HFTCBT\trade_data\20190321', sep=',')
trade_data_xbtusd = trade_data.loc[trade_data.symbol == 'XBTUSD'].copy()
orderbook_data = pd.read_csv(fr'C:\Users\a.acar\PycharmProjects\HFTCBT\quote_data\20190315_20190401.csv')
orderbook_data_xbtusd = orderbook_data.loc[orderbook_data.symbol == 'XBTUSD'].copy()

trade_data_xbtusd['timestamp'] = trade_data_xbtusd.timestamp.str.replace('D', ' ')
trade_data_xbtusd['timestamp'] = pd.to_datetime(trade_data_xbtusd['timestamp'], unit='ns')

orderbook_data_xbtusd['timestamp'] = orderbook_data_xbtusd.timestamp.str.replace('D', ' ')
orderbook_data_xbtusd['timestamp'] = pd.to_datetime(orderbook_data_xbtusd['timestamp'], unit='ns')
orderbook_data_xbtusd = orderbook_data_xbtusd.loc[(orderbook_data_xbtusd.timestamp >= '2019-03-21') &
                                                  (orderbook_data_xbtusd.timestamp < '2019-03-22')]

orderbook_data_xbtusd = orderbook_data_xbtusd.drop_duplicates('timestamp', keep='last')
orderbook_data_xbtusd[['previous_bidSize', 'previous_bidPrice', 'previous_askPrice', 'previous_askSize']] = orderbook_data_xbtusd[["bidSize", "bidPrice", "askPrice", "askSize"]].shift(1)
btc_tick_data = pd.merge(trade_data_xbtusd, orderbook_data_xbtusd, 'left', on='timestamp', suffixes=('', '_y'))
btc_tick_data.drop(['symbol_y'], axis=1, inplace=True)

N = 10000
N= len(btc_tick_data)
xx = btc_tick_data.head(N)
xx['side_numeric'] = xx['side'].replace(['Buy', 'Sell'], [0, 1])
xx['size_normalized'] = pd.qcut(xx['size'], 8, labels=False, duplicates='drop')
xx['volume'] = xx['size'] / xx['price']

# ilk olarak tradeler unique timestamp hale getirilecek
# ikinci olarak ilgili timestampte bekleyen order book hacimleri yanlarina kolon olarak eklenecektir.

# gecen hacim ve ilk kademe bekleyen hacimlerdeki iliskiler hareket olacagina dair bilgi verecektir.
# last nt araliginda gecen hacimde artis ve bekleyen hacimde artis olmamasi (belki de one gecmesi diyelim)
#  last nt de gecen hacim , last knt de ilk kademede bekleyen ortalama hacime gore fazlalaigi(yani trade var fakat bekleyen emirde duraksama var)


xy = xx.copy()

xy = xy.loc[:, ['timestamp', 'side', 'price', 'volume', 'size', 'homeNotional', 'tickDirection']]

xz = xy.groupby('timestamp').agg(
    side=('side', 'last'),
    volume=('volume', 'sum'),
    size=('size', 'sum'),
    homeNotional=('homeNotional', 'sum'),
    tickDirection=('tickDirection', 'last')
)
xz['intraday_time'] = xz.index.strftime("%H:%M")
xz['day'] = xz.index.floor('D')
xz['price'] = xz['size'].div(xz['volume'].values)

xz['previous_tick_direction'] = xz['tickDirection'].shift(1)
xz['previous_side'] = xz['side'].shift(1)

###
xz.groupby(['previous_side', 'side']).size() / xz.groupby(['previous_side']).size()

"""
previous_side  side
Buy            Buy     0.768
               Sell    0.231
Sell           Buy     0.386
               Sell    0.613
"""

xz.groupby(['previous_side', 'side', 'tickDirection']).size()
"""
previous_side  side  tickDirection
Buy            Buy   MinusTick           1
                     PlusTick            6
                     ZeroPlusTick     1300
               Sell  MinusTick         345
                     ZeroMinusTick      46
                     ZeroPlusTick        2
Sell           Buy   PlusTick          332
                     ZeroMinusTick       2
                     ZeroPlusTick       60
               Sell  MinusTick           2
                     ZeroMinusTick     622
                     ZeroPlusTick        1
"""

xz['side_numeric'] = xz['side'].replace(['Buy', 'Sell'], [0, 1])
xz['last_2_sell_side_count'] = xz['side_numeric'].shift(1).rolling(2).sum()
xz['last_3_sell_side_count'] = xz['side_numeric'].shift(1).rolling(3).sum()
xz['last_4_sell_side_count'] = xz['side_numeric'].shift(1).rolling(4).sum()
xz['last_5_sell_side_count'] = xz['side_numeric'].shift(1).rolling(5).sum()
xz['last_10_sell_side_count'] = xz['side_numeric'].shift(1).rolling(10).sum()
xz['last_20_sell_side_count'] = xz['side_numeric'].shift(1).rolling(20).sum()

for i in [20]:
    # for i in [2, 3, 4, 5, 10,20]:
    xz.groupby([f'last_{i}_sell_side_count', 'side']).size() / xz.groupby([f'last_{i}_sell_side_count']).size()
    ac = xz.groupby([f'last_{i}_sell_side_count', 'side']).size() / xz.groupby([f'last_{i}_sell_side_count']).size()
    print(pd.DataFrame(ac[slice(None), 'Buy'], columns=['Probability of Next MO being Buy MO']))

"""
                        Probability of Next MO being Buy MO
last_2_sell_side_count                                     
0.00                                                   0.82
1.00                                                   0.61
2.00                                                   0.24
                        Probability of Next MO being Buy MO
last_3_sell_side_count                                     
0.00                                                   0.86
1.00                                                   0.69
2.00                                                   0.44
3.00                                                   0.18
                        Probability of Next MO being Buy MO
last_4_sell_side_count                                     
0.00                                                   0.88
1.00                                                   0.74
2.00                                                   0.59
3.00                                                   0.32
4.00                                                   0.15
                        Probability of Next MO being Buy MO
last_5_sell_side_count                                     
0.00                                                   0.89
1.00                                                   0.78
2.00                                                   0.67
3.00                                                   0.44
4.00                                                   0.26
5.00                                                   0.13
                         Probability of Next MO being Buy MO
last_10_sell_side_count                                     
0.00                                                    0.91
1.00                                                    0.88
2.00                                                    0.77
3.00                                                    0.71
4.00                                                    0.63
5.00                                                    0.55
6.00                                                    0.45
7.00                                                    0.34
8.00                                                    0.24
9.00                                                    0.12
10.00                                                   0.12
"""
xz.groupby(['last_2_sell_side_count', 'side', 'tickDirection']).size()

xt = xz.reset_index()
xt['volume_normalized'] = pd.qcut(xt['volume'], 5, labels=False, duplicates='drop')
xt['side_numeric'] = xt['side'].replace(['Buy', 'Sell'], [0, 1])
xt.groupby(['volume_normalized', 'tickDirection']).size() / xt.groupby(['volume_normalized']).size()
"""
volume_normalized  tickDirection
0                  MinusTick        0.141
                   PlusTick         0.205
                   ZeroMinusTick    0.209
                   ZeroPlusTick     0.444
1                  MinusTick        0.134
                   PlusTick         0.160
                   ZeroMinusTick    0.195
                   ZeroPlusTick     0.510
2                  MinusTick        0.159
                   PlusTick         0.113
                   ZeroMinusTick    0.259
                   ZeroPlusTick     0.466
3                  MinusTick        0.148
                   PlusTick         0.093
                   ZeroMinusTick    0.267
                   ZeroPlusTick     0.489
4                  MinusTick        0.055
                   PlusTick         0.047
                   ZeroMinusTick    0.302
                   ZeroPlusTick     0.594
"""

xt.groupby(['volume_normalized','side']).size()