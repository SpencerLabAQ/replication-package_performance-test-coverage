# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

# %%
plots_path = r'../../figures'

# Loading coverage and time data
shortlisted_projects_JMH = pd.read_csv("../../inputs/projects_list/Projects_Shortlisted-JMH.csv")
shortlisted_projects_JUnit= pd.read_csv("../../inputs/projects_list/Projects_Shortlisted-JUnit.csv")

df = pd.read_csv("../../outputs/coverageJMH.csv")

size_data_JMH = df[['Project Name', 'Average Coverage']]
size_data_JMH = size_data_JMH.rename(columns={'Average Coverage': 'JMH Benchmarks'})
size_data_JMH = size_data_JMH[size_data_JMH['Project Name'].isin(shortlisted_projects_JMH['Project'])] 

df = pd.read_csv("../../outputs/coverageJUnit.csv")
size_data_JUnit = df[['Project Name', 'Average Coverage']]
size_data_JUnit = size_data_JUnit.rename(columns={'Average Coverage': 'JUnit Tests'})
size_data_JUnit = size_data_JUnit[size_data_JUnit['Project Name'].isin(shortlisted_projects_JUnit['Project'])]

#Merging and Sorting Data
merged_data = pd.merge(size_data_JMH, size_data_JUnit, left_on='Project Name', right_on='Project Name')
merged_data = merged_data.sort_values('Project Name', key=lambda x: x.str.lower(), ascending=True)

# Melt the data for grouped bar chart
data_melted = pd.melt(merged_data, id_vars='Project Name', var_name='Coverage Type', value_name='Coverage')

# Style and palette
sns.set_style('whitegrid')
sns.set_palette('dark')

plt.figure(figsize=(6.4, 4.8))
fig, ax = plt.subplots()
sns.barplot(x='Project Name', y='Coverage', hue='Coverage Type', data=data_melted, ax=ax).set(xlabel=None)
ax.legend(ncol=2, loc="upper right", frameon=True)
plt.ylabel('Scope')

plt.xticks(rotation=60, ha='right', fontsize=12, rotation_mode='anchor')
plt.ticklabel_format(style='plain', useOffset=False, axis='y')

# Adjust bottom margin and save the plot as pdf
#plt.subplots_adjust(bottom=0.2)

plt.tick_params(axis='x', which='major', pad=-3.5)
plt.tight_layout()
plt.savefig(os.path.join(plots_path,'plt_compare_test_size.pdf'), format='pdf',bbox_inches='tight')

# Show the plot
plt.show()


