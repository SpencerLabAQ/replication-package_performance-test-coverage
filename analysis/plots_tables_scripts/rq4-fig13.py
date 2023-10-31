import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import iqr
import warnings
import os
warnings.filterwarnings(action='ignore', category=FutureWarning)

#Average Execution Time Comparison

plots_path = r'../../figures'
m2b_summary = pd.read_csv('../../inputs/SummaryComparison.csv', sep = ';', decimal=",")

data = m2b_summary.rename(columns={"AVG JMH": "JMH Benchmarks", "AVG Junit": "JUnit Tests"})


# Melt the DataFrame 
df_melted = data.melt(id_vars='Project', value_vars=['JMH Benchmarks','JUnit Tests'])
data_sorted = df_melted.sort_values('Project', ascending=True)

# Style and palette
sns.set_style('whitegrid')
sns.set_palette('dark')

fig, ax = plt.subplots()
sns.barplot(x='Project', y='value', hue='variable', data=data_sorted, ax=ax).set(xlabel=None)
ax.legend(ncol=2, loc="upper right", frameon=True)

# Set the labels and title
plt.ylabel('Time in Seconds')
plt.xticks(rotation=60, ha='right', fontsize=12, rotation_mode='anchor')
plt.ticklabel_format(style='plain', useOffset=False, axis='y')
plt.tick_params(axis='x', which='major', pad=-3.5)
plt.tight_layout()
plt.yscale("log")

plt.savefig(os.path.join(plots_path,'jmh_junit_comparison_avg_time_real_log.pdf'), format='pdf', bbox_inches='tight')

# Show the plot
plt.show()