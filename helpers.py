from pathlib import Path
import matplotlib.pyplot as plt

def plot_daily_volume_by_month(stock, daily_metrics, img_output_path):
    bp = daily_metrics.boxplot(column=['DailyVolume'],
                               by=['month'],
                               figsize=(12, 8),
                               grid=False,
                               rot=45,
                               fontsize=8)

    bp.set_ylabel('DailyVolume')
    bp.set_xlabel('Month')
    bp.set_title(f'Ay Bazında Günlük Toplam Hacim Dağılımları ({stock})')
    path = Path(img_output_path) / Path(f'Daily_Volume_by_Month_{stock}.png')
    plt.savefig(path)
