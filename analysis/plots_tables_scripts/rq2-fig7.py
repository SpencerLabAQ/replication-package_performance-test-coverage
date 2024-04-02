# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# %%
#Used in the Paper
#Plotting JMH vs. JUnit Direct Coverage Graph

# %%
plots_path = r'../../figures'
tables_path = r'../../tables'

# %%
# Load the data
coverage_jmh = pd.read_csv('../../outputs/coverageJMH.csv')
coverage_jmh = coverage_jmh.rename(columns={'Direct Coverage Percentage': 'JMH Benchmarks'})
coverage_junit = pd.read_csv('../../outputs/coverageJUnit.csv')
coverage_junit = coverage_junit.rename(columns={'Direct Coverage Percentage': 'JUnit Tests'})

# Merge the data on 'Project Name'
merged_df = pd.merge(coverage_jmh, coverage_junit, on='Project Name')
df = merged_df[['Project Name', 'JMH Benchmarks', 'JUnit Tests']]

#sort the data frame by name of project
df = df.sort_values('Project Name', key=lambda x: x.str.lower(), ascending=True)

# Melt the DataFrame 
df_melted = df.melt(id_vars='Project Name', value_vars=['JMH Benchmarks', 'JUnit Tests'])

# Style and palette
sns.set_style('whitegrid')
sns.set_palette('colorblind')

plt.figure(figsize=(6.4, 4.8))
fig, ax = plt.subplots()
sns.barplot(x='Project Name', y='value', hue='variable', data=df_melted, ax=ax).set(xlabel=None)
ax.legend(ncol=2, loc="upper right", frameon=True)
plt.ylabel('Coverage (%)')

plt.xticks(rotation=60, ha='right', fontsize=12, rotation_mode='anchor')
plt.ticklabel_format(style='plain', useOffset=False, axis='y')

# Adjust bottom margin and save the plot as pdf
#plt.subplots_adjust(bottom=0.2)

plt.tick_params(axis='x', which='major', pad=-3.5)
plt.tight_layout()
plt.savefig(os.path.join(plots_path,'plt_directcoverage_compare_junit_jmh.pdf'), format='pdf',bbox_inches='tight')

# Show the plot
plt.show()


