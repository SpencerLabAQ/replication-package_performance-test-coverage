import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import iqr
import warnings
import os
warnings.filterwarnings(action='ignore', category=FutureWarning)


#JUNIT Total Execution Time
data = pd.read_csv('../../inputs/Summary.csv', sep = ';', decimal=",")
data["Time"] = data["Time"].astype(float)

data_sorted = data.sort_values('Project', ascending=True)

sns.set(style="whitegrid")
palette = 'colorblind'

# Create the plot
plt.figure(figsize=(6.4, 4.8))
plot = sns.barplot(x="Project", y="Time", data=data_sorted, palette=palette)
plt.ylabel("Time in seconds")
#plt.xlabel("Project Name")
#plt.title("JUnit testing time")
plt.xticks(rotation=60, ha='right', fontsize=12, rotation_mode='anchor')
plt.ticklabel_format(style='plain', useOffset=False, axis='y')
plt.axhline(y = 135.0,    # Line on y = 0.2
           xmin = 0.0, # From the left
           xmax = 1.0,
           linestyle ="dashed") # To the right

# Adjust bottom margin and save the plot as pdf
plt.subplots_adjust(bottom=0.2)
plt.yscale("log")
plt.savefig('junit_time_log.pdf', format='pdf')

plt.show()
