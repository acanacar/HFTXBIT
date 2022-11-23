import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pd.options.display.float_format = "{:,.2f}".format

data_xbtusd_processed = pd.read_pickle(fr'C:\Users\a.acar\PycharmProjects\HFTCBT\trade_data\xbtusd_20190101_20190528_processed.pkl')

data_xbtusd_processed['price'] = data_xbtusd_processed['size'].div(data_xbtusd_processed['volume'].values)

data_xbtusd_processed['previous_tick_direction'] = data_xbtusd_processed['tickDirection'].shift(1)
data_xbtusd_processed['previous_side'] = data_xbtusd_processed['side'].shift(1)

data_xbtusd_processed.groupby(['previous_side', 'side']).size() / data_xbtusd_processed.groupby(['previous_side']).size()
"""previous_side  side
Buy            Buy     0.667187
               Sell    0.332813
Sell           Buy     0.353828
               Sell    0.646172"""


data_xbtusd_processed.groupby(['previous_side', 'side', 'tickDirection']).size()/\
data_xbtusd_processed.groupby(['previous_side', 'side']).size()
'''
previous_side  side  tickDirection
Buy            Buy   MinusTick       0.01
                     PlusTick        0.01
                     ZeroMinusTick   0.01
                     ZeroPlusTick    0.97
               Sell  MinusTick       0.80
                     PlusTick        0.00
                     ZeroMinusTick   0.19
                     ZeroPlusTick    0.01
Sell           Buy   MinusTick       0.00
                     PlusTick        0.80
                     ZeroMinusTick   0.01
                     ZeroPlusTick    0.18
               Sell  MinusTick       0.01
                     PlusTick        0.01
                     ZeroMinusTick   0.97
                     ZeroPlusTick    0.01'''


data_xbtusd_processed['side_numeric'] = data_xbtusd_processed['side'].replace(['Buy', 'Sell'], [0, 1])
data_xbtusd_processed['last_2_sell_side_count'] = data_xbtusd_processed['side_numeric'].shift(1).rolling(2).sum()
data_xbtusd_processed['last_3_sell_side_count'] = data_xbtusd_processed['side_numeric'].shift(1).rolling(3).sum()
data_xbtusd_processed['last_4_sell_side_count'] = data_xbtusd_processed['side_numeric'].shift(1).rolling(4).sum()
data_xbtusd_processed['last_5_sell_side_count'] = data_xbtusd_processed['side_numeric'].shift(1).rolling(5).sum()
data_xbtusd_processed['last_10_sell_side_count'] = data_xbtusd_processed['side_numeric'].shift(1).rolling(10).sum()
data_xbtusd_processed['last_20_sell_side_count'] = data_xbtusd_processed['side_numeric'].shift(1).rolling(20).sum()
for i in [2, 3, 4, 5, 10, 20]:
    # data_xbtusd_processed.groupby([f'last_{i}_sell_side_count', 'side']).size() / data_xbtusd_processed.groupby([f'last_{i}_sell_side_count']).size()
    ac = data_xbtusd_processed.groupby([f'last_{i}_sell_side_count', 'side']).size() / data_xbtusd_processed.groupby([f'last_{i}_sell_side_count']).size()
    print(pd.DataFrame(ac[slice(None), 'Buy'], columns=['Probability of Next MO being Buy MO']))
"""                       Probability of Next MO being Buy MO
last_2_sell_side_count                                     
0.00                                                   0.74
1.00                                                   0.51
2.00                                                   0.27
                        Probability of Next MO being Buy MO
last_3_sell_side_count                                     
0.00                                                   0.79
1.00                                                   0.61
2.00                                                   0.41
3.00                                                   0.22
                        Probability of Next MO being Buy MO
last_4_sell_side_count                                     
0.00                                                   0.81
1.00                                                   0.67
2.00                                                   0.51
3.00                                                   0.34
4.00                                                   0.19
                        Probability of Next MO being Buy MO
last_5_sell_side_count                                     
0.00                                                   0.83
1.00                                                   0.72
2.00                                                   0.58
3.00                                                   0.44
4.00                                                   0.29
5.00                                                   0.17
                         Probability of Next MO being Buy MO
last_10_sell_side_count                                     
0.00                                                    0.88
1.00                                                    0.81
2.00                                                    0.75
3.00                                                    0.67
4.00                                                    0.59
5.00                                                    0.51
6.00                                                    0.42
7.00                                                    0.34
8.00                                                    0.26
9.00                                                    0.19
10.00                                                   0.11
                         Probability of Next MO being Buy MO
last_20_sell_side_count                                     
0.00                                                    0.91
1.00                                                    0.87
2.00                                                    0.84
3.00                                                    0.80
4.00                                                    0.76
5.00                                                    0.72
6.00                                                    0.68
7.00                                                    0.63
8.00                                                    0.59
9.00                                                    0.55
10.00                                                   0.50
11.00                                                   0.46
12.00                                                   0.42
13.00                                                   0.37
14.00                                                   0.33
15.00                                                   0.29
16.00                                                   0.24
17.00                                                   0.20
18.00                                                   0.16
19.00                                                   0.12
20.00                                                   0.08
"""
print(data_xbtusd_processed.groupby(['last_2_sell_side_count', 'side', 'tickDirection']).size() / data_xbtusd_processed.groupby(['last_2_sell_side_count', 'side']).size())
"""last_2_sell_side_count  side  tickDirection
0.00                    Buy   MinusTick       0.00
                              PlusTick        0.01
                              ZeroMinusTick   0.01
                              ZeroPlusTick    0.97
                        Sell  MinusTick       0.82
                              PlusTick        0.00
                              ZeroMinusTick   0.17
                              ZeroPlusTick    0.01
1.00                    Buy   MinusTick       0.00
                              PlusTick        0.40
                              ZeroMinusTick   0.01
                              ZeroPlusTick    0.58
                        Sell  MinusTick       0.40
                              PlusTick        0.00
                              ZeroMinusTick   0.59
                              ZeroPlusTick    0.01
2.00                    Buy   MinusTick       0.00
                              PlusTick        0.82
                              ZeroMinusTick   0.01
                              ZeroPlusTick    0.17
                        Sell  MinusTick       0.01
                              PlusTick        0.00
                              ZeroMinusTick   0.97
                              ZeroPlusTick    0.01
"""
xt = data_xbtusd_processed.reset_index()
xt['volume_normalized'] = pd.qcut(xt['volume'], 10, labels=False, duplicates='drop')
xt['side_numeric'] = xt['side'].replace(['Buy', 'Sell'], [0, 1])
print(xt.groupby(['volume_normalized', 'tickDirection']).size() / xt.groupby(['volume_normalized']).size())
"""volume_normalized  tickDirection
0                  MinusTick       0.19
                   PlusTick        0.20
                   ZeroMinusTick   0.28
                   ZeroPlusTick    0.33
1                  MinusTick       0.18
                   PlusTick        0.18
                   ZeroMinusTick   0.30
                   ZeroPlusTick    0.34
2                  MinusTick       0.18
                   PlusTick        0.18
                   ZeroMinusTick   0.30
                   ZeroPlusTick    0.33
3                  MinusTick       0.17
                   PlusTick        0.17
                   ZeroMinusTick   0.31
                   ZeroPlusTick    0.35
4                  MinusTick       0.16
                   PlusTick        0.16
                   ZeroMinusTick   0.32
                   ZeroPlusTick    0.35
5                  MinusTick       0.15
                   PlusTick        0.15
                   ZeroMinusTick   0.34
                   ZeroPlusTick    0.36
6                  MinusTick       0.14
                   PlusTick        0.14
                   ZeroMinusTick   0.35
                   ZeroPlusTick    0.37
7                  MinusTick       0.12
                   PlusTick        0.12
                   ZeroMinusTick   0.37
                   ZeroPlusTick    0.39
8                  MinusTick       0.09
                   PlusTick        0.09
                   ZeroMinusTick   0.40
                   ZeroPlusTick    0.42
9                  MinusTick       0.05
                   PlusTick        0.05
                   ZeroMinusTick   0.44
                   ZeroPlusTick    0.45"""

FREQ = '5S'
data_xbtusd_processed['side_numeric_type2'] = data_xbtusd_processed['side'].replace(['Buy', 'Sell'], [1, -1])
data_xbtusd_processed['signed_volume'] = data_xbtusd_processed['volume'] * data_xbtusd_processed['side_numeric_type2']
size_volume_5s = data_xbtusd_processed[['size', 'volume', 'signed_volume']].resample(FREQ, label='right').sum()
size_volume_5s['count_of_tick'] = data_xbtusd_processed['volume'].resample(FREQ, label='right').count()
price_last = data_xbtusd_processed['price'].resample(FREQ, label='right').last()
price_first = data_xbtusd_processed['price'].resample(FREQ, label='right').first()

size_volume_5s['volume_normalized'] = pd.qcut(size_volume_5s['volume'], 8, labels=False, duplicates='drop')
size_volume_5s['next_interval_volume_normalized'] = size_volume_5s['volume_normalized'].shift(-1)
size_volume_5s['signed_volume_normalized'] = pd.qcut(size_volume_5s['signed_volume'], 8, labels=False, duplicates='drop')
size_volume_5s['sign_of_volume'] = np.sign(size_volume_5s['signed_volume'])
size_volume_5s['next_sign_of_volume'] = size_volume_5s['sign_of_volume'].shift(-1)
size_volume_5s['last_sign_of_volume'] = size_volume_5s['sign_of_volume'].shift(1)

for col_ in ['volume', 'count_of_tick', 'signed_volume']:
    for i_ in [1, 2, 3]:
        size_volume_5s[f'next_{i_}_interval_total_{col_}'] = size_volume_5s[col_].shift(-i_).rolling(i_).sum()
        size_volume_5s[f'next_{i_}_interval_avg_{col_}'] = size_volume_5s[col_].shift(-i_).rolling(i_).mean()
        size_volume_5s[f'last_{i_}_interval_total_{col_}'] = size_volume_5s[col_].shift(1).rolling(i_).sum()
        size_volume_5s[f'last_{i_}_interval_avg_{col_}'] = size_volume_5s[col_].shift(1).rolling(i_).mean()


size_volume_5s['tick_f'] = size_volume_5s['count_of_tick'] != 0
size_volume_5s['tick_f'] = size_volume_5s['tick_f'].map({True: 1, False: 0})
size_volume_5s['last_2_tick_f'] = size_volume_5s['tick_f'].shift(1).rolling(2).sum()
size_volume_5s['last_1_tick_f'] = size_volume_5s['tick_f'].shift(1).rolling(1).sum()
size_volume_5s['next_1_tick_f'] = size_volume_5s['tick_f'].shift(-1).rolling(1).sum()
size_volume_5s['next_2_tick_f'] = size_volume_5s['tick_f'].shift(-2).rolling(2).sum()


"""5 snlik periyotta islem adedi ile bir sonraki 5 snlik periyottaki islem adedi dogru orantilidir."""
print(size_volume_5s.groupby(['count_of_tick'])['next_1_interval_total_count_of_tick'].mean())

print(size_volume_5s.groupby(['volume_normalized'])['next_1_interval_total_volume'].mean())
"""volume_normalized
0    4.15
1    5.44
2    7.11
3    9.35
4   12.27
5   17.79
6   27.98
7   73.75"""

print(size_volume_5s.groupby(['signed_volume_normalized'])['next_1_interval_total_signed_volume'].mean())

"""
signed_volume_normalized
0   -26.33
1    -5.91
2    -2.18
3    -0.30
4     1.04
5     2.81
6     6.67
7    25.27"""

size_volume_5s.groupby(['count_of_tick'])['next_1_interval_total_count_of_tick'].mean().sort_index().plot()
plt.savefig(fr'C:\Users\a.acar\PycharmProjects\HFTCBT\outputs\Next Count of Tick given Current Count Of tick XBTUSD from 2019-01.png')


size_volume_5s.groupby(['last_2_tick_f', 'last_1_tick_f', 'tick_f']).size() / size_volume_5s.groupby(['last_2_tick_f', 'last_1_tick_f']).size()
size_volume_5s.groupby(['last_2_tick_f', 'tick_f', 'next_1_tick_f']).size() / size_volume_5s.groupby(['last_2_tick_f', 'tick_f']).size()
size_volume_5s.groupby(['last_2_tick_f', 'tick_f', 'volume_normalized'])['next_interval_volume_normalized'].mean()

size_volume_5s.groupby(['last_1_tick_f', 'tick_f']).size() / size_volume_5s.groupby(['last_1_tick_f']).size()

"""
5 sn boyunca transaction olmamis durumda, bir sonraki 5 sn icinde transaction olma ihtimali daha fazladir.
last_1_tick_f  tick_f
0.00           0        0.27
               1        0.73
1.00           0        0.07
               1        0.93"""

size_volume_5s.groupby(['last_sign_of_volume', 'sign_of_volume', 'next_sign_of_volume']).size() / \
size_volume_5s.groupby(['last_sign_of_volume', 'sign_of_volume']).size()
'''last_sign_of_volume  sign_of_volume  next_sign_of_volume
-1.00                -1.00           -1.00                 0.73
                                     0.00                  0.05
                                     1.00                  0.22
                     0.00            -1.00                 0.47
                                     0.00                  0.24
                                     1.00                  0.29
                     1.00            -1.00                 0.41
                                     0.00                  0.07
                                     1.00                  0.51
0.00                 -1.00           -1.00                 0.48
                                     0.00                  0.23
                                     1.00                  0.29
                     0.00            -1.00                 0.33
                                     0.00                  0.34
                                     1.00                  0.32
                     1.00            -1.00                 0.29
                                     0.00                  0.22
                                     1.00                  0.49
1.00                 -1.00           -1.00                 0.49
                                     0.00                  0.07
                                     1.00                  0.44
                     0.00            -1.00                 0.29
                                     0.00                  0.24
                                     1.00                  0.47
                     1.00            -1.00                 0.21
                                     0.00                  0.05
                                     1.00                  0.75
dtype: float64'''
