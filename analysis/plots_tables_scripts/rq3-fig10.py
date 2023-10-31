import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import iqr
import warnings
import os
warnings.filterwarnings(action='ignore', category=FutureWarning)

plots_path = r'../../figures'
data = pd.read_csv('../../inputs/summaryAlignedDataset.csv')
data["Time"] = data["Time"].astype(float)/3600

data_sorted = data.sort_values('Project', ascending=True)
sns.set(style="whitegrid")
palette = 'viridis'


plt.figure(figsize=(6.4, 4.8))
plot = sns.barplot(x="Project", y="Time", data=data_sorted, palette=palette).set(xlabel=None)
plt.ylabel("Time in hours")

plt.xticks(rotation=60, ha='right', fontsize=12, rotation_mode='anchor')
plt.ticklabel_format(style='plain', useOffset=False, axis='y')
plt.yscale("log")
plt.axhline(y = 29.3, xmin = 0.0,xmax = 1.0,linestyle ="dashed")
plt.subplots_adjust(bottom=0.2)
plt.tick_params(axis='x', which='major', pad=-5.0)
plt.tight_layout()
plt.savefig(os.path.join(plots_path,'jmh_time_log.pdf'), format='pdf', bbox_inches='tight')

plt.show()