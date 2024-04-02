import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import iqr
import warnings
import os
warnings.filterwarnings(action='ignore', category=FutureWarning)

#Used in the Paper
#Plotting JMH average execution time

plots_path = r'../../figures'
data = pd.read_csv('../../inputs/benchmarks/summaryAlignedDataset.csv')
data["Time"] = data["Time"].astype(float)/3600

# Sort the data in ascending order by the percentage of benchmarked methods
data_sorted = data.sort_values("Project", ascending=True)

#Set the style of the plots
sns.set(style="whitegrid")
# Define a palette
palette = 'colorblind'

#Create the plot
plt.figure(figsize=(6.4, 4.8))
plot = sns.barplot(x="Project", y="Time_per_Benchmark", data=data_sorted, palette=palette).set(xlabel=None)


plt.ylabel("Time in seconds")
plt.xticks(rotation=60, ha='right', fontsize=12, rotation_mode='anchor')
plt.ticklabel_format(style='plain', useOffset=False, axis='y')
plt.yscale("log")
plt.axhline(y = 1391.12,xmin = 0.0,xmax = 1.0,linestyle ="dashed")

plt.tick_params(axis='x', which='major', pad=-5.0)
plt.tight_layout()
os.path.join(plots_path,'jmh_average_time.pdf')
plt.savefig(os.path.join(plots_path,'jmh_average_time.pdf'), format='pdf', bbox_inches='tight')

plt.show()
