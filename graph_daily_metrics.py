import pandas as pd
import matplotlib.pyplot as plt

data_xbtusd_processed = pd.read_pickle(fr'C:\Users\a.acar\PycharmProjects\HFTCBT\trade_data\xbtusd_20190101_20190528_processed.pkl')

data_xbtusd_processed.groupby(['month'])['volume'].sum()

daily_volume_data = pd.DataFrame(data_xbtusd_processed.groupby(['day'])['volume'].sum())
daily_volume_data['month'] = daily_volume_data.index.strftime('%Y-%m')

intraday_timely_volume_data = data_xbtusd_processed.groupby('intraday_time_h')['volume'].sum()
gb_month_day_h = data_xbtusd_processed.groupby(['month', 'day', 'intraday_time_h'])['volume'].sum()
# gb_month_h = data_xbtusd_processed.groupby(['month', 'intraday_time_h'])['volume'].sum() / data_xbtusd_processed.groupby(['month'])['volume'].sum()

daily_total_volume_by_hour_as_pct = gb_month_day_h / gb_month_day_h.groupby(level=['month', 'day']).sum()

#   BOXPLOT SAATLIK VOLUME AS PCT FOR SIX MONTHS
bp = daily_total_volume_by_hour_as_pct.unstack(level=2).boxplot(
    figsize=(12, 8),
    grid=False,
    rot=45, fontsize=8)
bp.set_ylabel('Percentage of Total Daily Volume')
bp.set_xlabel('Hour')
bp.set_title(f"Saat Bazinda Gunluk Hacmin ortalama Yuzde Kaci XBTUSD from 20190101 to 20190528.png")
plt.savefig(fr'C:\Users\a.acar\PycharmProjects\HFTCBT\outputs\Saat Bazinda Gunluk Hacmin ortalama Yuzde Kaci XBTUSD from 20190101 to 20190528.png')
plt.close()

#   BOXPLOT SAATLIK VOLUME AS PCT FOR EACH MONTH

for month_ in daily_total_volume_by_hour_as_pct.index.get_level_values(0).unique().values:
    bp = daily_total_volume_by_hour_as_pct.unstack(level=2).loc[(month_, slice(None))].boxplot(
        figsize=(12, 8),
        grid=False,
        rot=45, fontsize=8)
    bp.set_ylabel(f'Percentage of Total Daily Volume')
    bp.set_xlabel('Hour')
    bp.set_title(f"Saat Bazinda Gunluk Hacmin ortalama Yuzde Kaci XBTUSD from {month_}.png")
    plt.savefig(fr'C:\Users\a.acar\PycharmProjects\HFTCBT\outputs\Saat Bazinda Gunluk Hacmin ortalama Yuzde Kaci XBTUSD from {month_}.png')
    plt.close()

#   BOXPLOT DAILY VOLUME BY MONTHS
bp = daily_volume_data.boxplot(column=['volume'],
                               by=['month'],
                               figsize=(12, 8),
                               grid=False,
                               rot=45,
                               fontsize=8)

bp.set_ylabel('DailyVolume')
bp.set_xlabel('Month')
bp.set_title(f'Ay Bazında Günlük Toplam Hacim Dağılımları XBTUSD)')
plt.savefig(fr'C:\Users\a.acar\PycharmProjects\HFTCBT\outputs\Ay Bazında Günlük Toplam Hacim Dağılımları XBTUSD.png')
plt.close()

#   Daily Total Volume of XBTUSD from 20190101 to 20190528.png
daily_volume_data.plot()
plt.tight_layout()
plt.title('Daily Total Volume of XBTUSD from 20190101 to 20190528')
plt.savefig(fr'C:\Users\a.acar\PycharmProjects\HFTCBT\outputs\Daily Total Volume of XBTUSD from 20190101 to 20190528.png')
plt.close()

#   Daily Total Size of XBTUSD from 20190101 to 20190528.png
daily_size_data = pd.DataFrame(data_xbtusd_processed.groupby(['day'])['size'].sum())

daily_size_data.plot()
plt.tight_layout()
plt.title('Daily Total Size of XBTUSD from 20190101 to 20190528')
plt.savefig(fr'C:\Users\a.acar\PycharmProjects\HFTCBT\outputs\Daily Total Size of XBTUSD from 20190101 to 20190528.png')
plt.close()
