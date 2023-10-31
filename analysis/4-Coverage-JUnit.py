# %%
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import iqr
import warnings
import os
warnings.filterwarnings(action='ignore', category=FutureWarning)

# %%
# Load the CSV files into dataframes
df_methods_to_bench = pd.read_csv("../inputs/wrangled/m2u/00_combined_methods_to_test_summary.csv")
df_bench_to_methods_summary = pd.read_csv("../inputs/wrangled/u2m/00_combined_test_to_methods_summary.csv")
df_bench_to_methods_detail = pd.read_csv("../inputs/wrangled/u2m/00_combined_test_to_methods.csv")
# Dropping rows where 'Methods' column is NaN in the details dataframe
df_bench_to_methods_detail = df_bench_to_methods_detail.dropna(subset=['Methods'])

df_overlap_ratios = pd.read_csv("../outputs/Overlap_Ratios_Junit.csv")

# %%
# Merging dataframes to ensure correct alignment of project names
df_merged = df_methods_to_bench.merge(df_bench_to_methods_summary, on='Project Name', how='left')
df_merged = df_merged.merge(df_overlap_ratios, on='Project Name', how='left')

# Creating a new dataframe for the statistics table
df_statistics = pd.DataFrame()

# Getting Project Name, Total Methods, and Methods Covered from the summary dataframes
df_statistics['Project Name'] = df_merged['Project Name']
df_statistics['Total Methods'] = df_merged['Methods']
df_statistics['Methods Covered'] = df_merged['Tested']
df_statistics['Methods Directly Covered'] = df_merged['Directly Tested']
df_statistics['Coverage Percentage'] = ((df_statistics['Methods Covered'] / df_statistics['Total Methods']) * 100).round(2)
df_statistics['Direct Coverage Percentage'] = ((df_statistics['Methods Directly Covered'] / df_statistics['Total Methods']) * 100).round(2)
df_statistics['Total Tests'] = df_merged['Total Tests']
df_statistics['Overlap Ratio'] = df_merged['Overlap Ratio']
df_statistics['Methods Tested'] = df_merged['Methods Tested']
df_statistics['Methods Directly Tested'] = df_merged['Methods Directly Tested']
df_statistics['Average Coverage'] = (df_merged['Methods Tested'] / df_merged['Total Tests']).round(2)

df_statistics


# %%
df_statistics.to_csv(r'../outputs/coverageJUnit.csv', index=False)


