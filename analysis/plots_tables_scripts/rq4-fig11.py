import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import iqr
import warnings
import os
warnings.filterwarnings(action='ignore', category=FutureWarning)

#Execution Time Comparison

plots_path = r'../../figures'
time_jmh = pd.read_csv('../../inputs/benchmarks/summaryAlignedDataset.csv')
time_junit = pd.read_csv('../../inputs/unit_tests/summary.csv')


# Load the data
time_junit = time_junit.groupby('Project').agg({'Time': 'sum'}).reset_index()

time_jmh["Time"] = time_jmh['Time'].astype(float)
time_junit["Time"] = time_junit["Time"].astype(float)

# Merge the data on 'Project'
merged_df = pd.merge(pd.DataFrame(time_jmh), pd.DataFrame(time_junit), on='Project')
df = pd.DataFrame(merged_df)
df.rename(columns = {'Time_x':'JMH Benchmarks', 'Time_y':'JUnit Tests'}, inplace = True)

# Melt the DataFrame 
df_melted = df.melt(id_vars='Project', value_vars=['JMH Benchmarks', 'JUnit Tests'])
data_sorted = df_melted.sort_values('Project', ascending=True)


# Style and palette
sns.set_style('whitegrid')
sns.set_palette('colorblind')

plt.figure(figsize=(6.4, 4.8))

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

plt.savefig(os.path.join(plots_path,'jmh_junit_comparison_time_real_log.pdf'), format='pdf', bbox_inches='tight')

# Show the plot
plt.show()