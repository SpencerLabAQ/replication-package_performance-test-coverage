# %%
import pandas as pd
from itertools import combinations
from collections import defaultdict
import os

# %%
# Function to read and process the combined benchmark to methods data
def read_bm_to_methods(filename):
    df = pd.read_csv(filename)
    df['Methods'] = df['Methods'].str.split(',')
    df = df.explode('Methods')
    df['Methods'] = df['Methods'].str.strip()
    df = df[df['Methods'] != '']  # Remove empty strings
    return df

# Function to read and process the combined methods to benchmarks data
def read_methods_to_bm(filename):
    df = pd.read_csv(filename)
    df['Benchmarked_by'] = df['Benchmarked_by'].str.split(',')
    df = df.explode('Benchmarked_by')
    df['Benchmarked_by'] = df['Benchmarked_by'].str.strip()
    return df

# Function to calculate the Overlap Ratio for a given project
def calculate_overlap_ratio(df):
    benchmarks = df.groupby('Benchmark Name')['Methods'].apply(set)
    intersections = set()
    union = set()
    for bm1, bm2 in combinations(benchmarks.index, 2):
        intersection = benchmarks[bm1] & benchmarks[bm2]
        intersections |= intersection
        union |= benchmarks[bm1] | benchmarks[bm2]
    return len(intersections) / len(union) if union else 0

# Main script
if __name__ == "__main__":
    # Read the combined data

    df_bm_to_methods = read_bm_to_methods("../inputs/wrangled/b2m/00_combined_bench_to_methods.csv")
    df_methods_to_bm = read_methods_to_bm("../inputs/wrangled/m2b/00_combined_methods_to_bench.csv")

    # Calculate the Overlap Ratio for each project
    overlap_ratios = {}
    for project in df_bm_to_methods['Project Name'].unique():
        df_project = df_bm_to_methods[df_bm_to_methods['Project Name'] == project]
        overlap_ratios[project] = calculate_overlap_ratio(df_project)

    # Create a DataFrame from the Overlap Ratios
    df_overlap_ratios = pd.DataFrame.from_dict(overlap_ratios, orient='index', columns=['Overlap Ratio'])

    # Rename the first column to 'Project Name'
    df_overlap_ratios = df_overlap_ratios.rename_axis('Project Name').reset_index()

    # Format the Overlap Ratio to display two decimal places
    df_overlap_ratios['Overlap Ratio'] = df_overlap_ratios['Overlap Ratio'].map('{:.2f}'.format)

    df_overlap_ratios.to_csv("../outputs/Overlap_Ratios_JMH.csv", index=False)
    # Print the DataFrame
    print(df_overlap_ratios)

    


