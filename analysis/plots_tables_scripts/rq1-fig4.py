# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os

# %%
#Used in the Paper
#Plotting Direct JMH Coverage Graph

plots_path = r'../../figures'
coverage_path = "../../outputs/coverageJMH.csv"
df_merged_statistics = pd.read_csv(coverage_path)

# Set the style of the plots
sns.set(style="whitegrid")

palette = 'viridis'
plt.figure(figsize=(6.4, 4.8))
plot = sns.barplot(x="Project Name", y="Direct Coverage Percentage", data=df_merged_statistics, palette=palette).set(xlabel=None)
plt.ylabel("Benchmark Coverage (%)")

plt.xticks(rotation=60, ha='right', fontsize=12, rotation_mode='anchor')
plt.ticklabel_format(style='plain', useOffset=False, axis='y')

# Adjust bottom margin and save the plot as pdf
#plt.subplots_adjust(bottom=0.2)

plt.tick_params(axis='x', which='major', pad=-3.5)
plt.tight_layout()
plt.savefig(os.path.join(plots_path,'plt_coverage_direct_jmh.pdf'), format='pdf',bbox_inches='tight')

# Show the plot
plt.show()


