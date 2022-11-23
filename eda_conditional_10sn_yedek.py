
size_volume_10s = data_xbtusd_processed[['size', 'volume']].resample('10S', label='right').sum()
size_volume_10s['count_of_tick'] = data_xbtusd_processed['volume'].resample('10S', label='right').count()
price_last = data_xbtusd_processed['price'].resample('10S', label='right').last()
price_first = data_xbtusd_processed['price'].resample('10S', label='right').first()

size_volume_10s_vol_f = pd.DataFrame(size_volume_10s['volume'] == 0)
size_volume_10s_vol_f.columns = ['tick_f']
size_volume_10s_vol_f['previous_tick_f'] = size_volume_10s_vol_f['tick_f'].shift(1)
size_volume_10s_vol_f['previous2_tick_f'] = size_volume_10s_vol_f['tick_f'].shift(2)
size_volume_10s['next_interval_count_of_tick'] = size_volume_10s['count_of_tick'].shift(-1)
size_volume_10s['next_2_interval_total_count_of_tick'] = size_volume_10s['count_of_tick'].shift(-1).rolling(2).sum()
size_volume_10s['next_2_interval_avg_count_of_tick'] = size_volume_10s['count_of_tick'].shift(-1).rolling(2).mean()
size_volume_10s['next_3_interval_total_count_of_tick'] = size_volume_10s['count_of_tick'].shift(-1).rolling(3).sum()
size_volume_10s['next_3_interval_avg_count_of_tick'] = size_volume_10s['count_of_tick'].shift(-1).rolling(3).mean()

size_volume_10s['next_interval_volume'] = size_volume_10s['volume'].shift(-1)
size_volume_10s['next_2_interval_total_volume'] = size_volume_10s['volume'].shift(-1).rolling(2).sum()
size_volume_10s['next_2_interval_avg_volume'] = size_volume_10s['volume'].shift(-1).rolling(2).mean()
size_volume_10s['next_3_interval_total_volume'] = size_volume_10s['volume'].shift(-1).rolling(3).sum()
size_volume_10s['next_3_interval_avg_volume'] = size_volume_10s['volume'].shift(-1).rolling(3).mean()

size_volume_10s_vol_f.groupby(['previous_tick_f', 'tick_f']).size() / size_volume_10s_vol_f.groupby(['previous_tick_f']).size()
"""
10 sn boyunca transaction olmamis durumda, bir sonraki 10 sn icinde transaction olma ihtimali daha fazladir.
previous_tick_f  tick_f
False            False    0.98
                 True     0.02
True             False    0.87
                 True     0.13"""

size_volume_10s_vol_f.groupby(['previous2_tick_f', 'previous_tick_f', 'tick_f']).size() / size_volume_10s_vol_f.groupby(['previous2_tick_f', 'previous_tick_f']).size()
"""previous2_tick_f  previous_tick_f  tick_f
False             False            False    0.98
                                   True     0.02
                  True             False    0.88
                                   True     0.12
True              False            False    0.90
                                   True     0.10
                  True             False    0.81
                                   True     0.19"""

size_volume_10s[list(size_volume_10s_vol_f.columns)] = size_volume_10s_vol_f.values
size_volume_10s.groupby(['previous2_tick_f', 'previous_tick_f', 'tick_f'])['volume'].mean()
size_volume_10s.groupby(['previous2_tick_f', 'previous_tick_f', 'tick_f'])['volume'].quantile()

"""Son 20 snde total hacim/Son 40 snde total hacim orani 1'e yakinsadikca devamindaki 20'snde olan hacim ortalama 20sn'de olan hacme gore fazladir."""

size_volume_10s['last_10sn_total_volume'] = size_volume_10s['volume'].shift(1).rolling(1).sum()
size_volume_10s['last_20sn_total_volume'] = size_volume_10s['volume'].shift(1).rolling(2).sum()
size_volume_10s['last_40sn_total_volume'] = size_volume_10s['volume'].shift(1).rolling(4).sum()
size_volume_10s['ratio_total_volume_last_10sn_to_20sn'] = size_volume_10s['last_10sn_total_volume'] / size_volume_10s['last_20sn_total_volume']
size_volume_10s['ratio_total_volume_last_20sn_to_40sn'] = size_volume_10s['last_20sn_total_volume'] / size_volume_10s['last_40sn_total_volume']
size_volume_10s['ratio_total_volume_last_10sn_to_20sn_normalized'] = pd.qcut(size_volume_10s['ratio_total_volume_last_10sn_to_20sn'], 10, labels=False, duplicates='drop')
size_volume_10s['ratio_total_volume_last_20sn_to_40sn_normalized'] = pd.qcut(size_volume_10s['ratio_total_volume_last_20sn_to_40sn'], 10, labels=False, duplicates='drop')

print(size_volume_10s.groupby(['ratio_total_volume_last_10sn_to_20sn_normalized'])['next_interval_count_of_tick'].mean())
print(size_volume_10s.groupby(['ratio_total_volume_last_20sn_to_40sn_normalized'])['next_interval_count_of_tick'].mean())
