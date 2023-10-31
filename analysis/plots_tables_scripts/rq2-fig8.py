# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# %%
plots_path = r'../../figures'

# %%
# Load the data
overlap_ratios_junit = pd.read_csv(r'../../outputs/coverageJUnit.csv')
overlap_ratios_benchmark = pd.read_csv(r'../../outputs/coverageJMH.csv')

# Rename the columns
overlap_ratios_junit.rename(columns={'Overlap Ratio': 'JUnit Tests'}, inplace=True)
overlap_ratios_benchmark.rename(columns={'Overlap Ratio': 'JMH Benchmarks'}, inplace=True)

# Merge and sort the data
overlap_ratios = pd.merge(overlap_ratios_junit, overlap_ratios_benchmark, on='Project Name')
overlap_ratios = overlap_ratios.sort_values('Project Name', key=lambda x: x.str.lower(), ascending=True)

# Melt the DataFrame 
df_melted = overlap_ratios.melt(id_vars='Project Name', value_vars=['JMH Benchmarks', 'JUnit Tests'])

# Style and palette
sns.set_style('whitegrid')
sns.set_palette('dark')

plt.figure(figsize=(6.4, 4.8))
fig, ax = plt.subplots()
sns.barplot(x='Project Name', y='value', hue='variable', data=df_melted, ax=ax).set(xlabel=None)
ax.legend(ncol=2, loc="upper right", frameon=True)
plt.ylabel('Coverage Overlap Ratio')

plt.xticks(rotation=60, ha='right', fontsize=12, rotation_mode='anchor')
plt.ticklabel_format(style='plain', useOffset=False, axis='y')

# Adjust bottom margin and save the plot as pdf
#plt.subplots_adjust(bottom=0.2)

plt.tick_params(axis='x', which='major', pad=-3.5)
plt.tight_layout()
plt.savefig(os.path.join(plots_path,'plt_overlapratio_compare_junit_jmh.pdf'), format='pdf',bbox_inches='tight')

# Show the plot
plt.show()


