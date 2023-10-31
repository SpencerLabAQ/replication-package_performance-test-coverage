# %%
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# %%
#Plotting Overlap Ratios JMH

plots_path = r'../../figures'
tables_path = r'../../tables'

# Set the style of the plots
sns.set(style="whitegrid")
palette = 'viridis'

overlap_ratios_path = "../../outputs/Overlap_Ratios_JMH.csv"
df_overlap_ratios = pd.read_csv(overlap_ratios_path)

# Convert the Overlap Ratio column back to numeric if it's not already
df_overlap_ratios['Overlap Ratio'] = pd.to_numeric(df_overlap_ratios['Overlap Ratio'])

plt.figure(figsize=(6.4, 4.8))
plot = sns.barplot(x=df_overlap_ratios['Project Name'], y=df_overlap_ratios['Overlap Ratio'], palette=palette).set(xlabel=None)
plt.ylabel('Overlap Ratio')

plt.xticks(rotation=60, ha='right', fontsize=12, rotation_mode='anchor')
plt.ticklabel_format(style='plain', useOffset=False, axis='y')


plt.tick_params(axis='x', which='major', pad=-3.5)
plt.tight_layout()
plt.savefig(os.path.join(plots_path,'plt_overlap_ratio.pdf'), format='pdf',bbox_inches='tight')

# Show the plot
plt.show()


