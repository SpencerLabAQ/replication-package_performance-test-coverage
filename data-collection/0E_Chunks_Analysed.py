# %%
import os
import pandas as pd
import glob
import numpy as np
from collections import defaultdict
import argparse

# %%
def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

# %%
def get_direct_calls_set(input_array, in_set):
    output_set = set()
    skip_flag = False
    for i in input_array:
        if skip_flag and i != '#':
            continue
        elif i == '#':
            skip_flag = False
        elif i in in_set:
            output_set.add(i)
            skip_flag = True
    return output_set


def combine_csv_files(csvs_path, output_path):
    extension = 'csv'
    all_filenames = [os.path.join(csvs_path, f) for f in glob.glob(os.path.join(csvs_path, f'*.{extension}'))]
    combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames])
    combined_csv.to_csv(output_path, index=False, encoding='utf-8-sig')
    return output_path

# %%
def create_method_dictionaries(aggregated_df):
    # Convert DataFrame to Dictionary for faster iteration
    df_dict = aggregated_df.to_dict('records')

    # Create a defaultdict of lists
    methods_dict = defaultdict(list)
    direct_methods_dict = defaultdict(list)

    for row in df_dict:
        methods = row['Methods'].split(',')
        direct_methods = row['Direct Methods'].split(',')
        for method in methods:
            if method:  # avoid empty strings
                methods_dict[method].append(row['Benchmark Name'])
    
        for direct_method in direct_methods:
            if direct_method:  # avoid empty strings
                direct_methods_dict[direct_method].append(row['Benchmark Name'])

    # Convert back to regular dictionary
    methods_dict = dict(methods_dict)
    direct_methods_dict = dict(direct_methods_dict)

    return methods_dict, direct_methods_dict


# %%
def methods_to_benchmarks_analysis(project_name, methods_set, methods_dict, direct_methods_dict, output_path2):
    result_list = []

    for method in methods_set:
        is_benchmarked = int(method in methods_dict)
        is_directly_benchmarked = int(method in direct_methods_dict)
        benchmark_count = len(methods_dict[method]) if is_benchmarked else 0
        direct_benchmark_count = len(direct_methods_dict[method]) if is_directly_benchmarked else 0
        benchmarked_by = ','.join(methods_dict[method]) if is_benchmarked else ''
        directly_benchmarked_by = ','.join(direct_methods_dict[method]) if is_directly_benchmarked else ''

        result_dict = {'Project Name': project_name,
                       'Method': method,
                       'is_Benchmarked': is_benchmarked,
                       'is_Directly_Benchmarked': is_directly_benchmarked,
                       'Benchmark_Count': benchmark_count,
                       'Direct_Benchmark_Count': direct_benchmark_count,
                       'Benchmarked_by': benchmarked_by,
                       'Directly_Benchmarked_By': directly_benchmarked_by}

        result_list.append(result_dict)

    result_df = pd.DataFrame(result_list)
    # Save the aggregated DataFrame to a CSV file
    create_directory_if_not_exists(output_path2)
    result_df.to_csv(os.path.join(output_path2, f"{project_name}.csv"), index=False)
    
    return result_df

# %%
def aggregate_output(project, output_folder):
    # Get a list of all CSV files in the output directory
    csv_files = glob.glob(os.path.join(output_folder,project, "*.csv"))

    # Initialize a list to store DataFrames
    df_list = []

    # Read each CSV file and append it to the list
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)
        if not df.empty:
            df_list.append(df)

    # Concatenate all DataFrames
    combined_df = pd.concat(df_list, ignore_index=True)

    # Handle NaN values in 'Methods' and 'Direct Methods' columns
    # combined_df['Methods'] = combined_df['Methods'].replace(np.nan, '')
    combined_df = combined_df.fillna('')

    # combined_df['Direct Methods'] = combined_df['Direct Methods'].replace(np.nan, '')

    # Groupby 'Project Name' and 'Benchmark Name' and aggregate 'Count', 'Direct Count', 'Methods' and 'Direct Methods'
    aggregated_df = combined_df.groupby(['Project Name', 'Benchmark Name']).agg({
        'Count': 'max',
        'Direct Count': 'max',
        'Methods': lambda x: ','.join(set(','.join(x).split(','))).strip(),
        'Direct Methods': lambda x: ','.join(set(','.join(x).split(','))).strip()
    }).reset_index()

    # Save the aggregated DataFrame to a CSV file
    create_directory_if_not_exists(output_folder)
    aggregated_df.to_csv(os.path.join(output_folder, f"{project}.csv"), index=False)

    return aggregated_df

# %%
def process_chunk(project_name, chunk_file_path, project_benchmarks, methods_set):
    
    # Initialize a list to store the results
    result_list = []

    # Initialize a new dataframe to store the results
    result_df = pd.DataFrame(columns=['Project Name', 'Benchmark Name', 'Count', 'Direct Count', 'Methods', 'Direct Methods'])
        
    # Read the CSV file
    chunk_df = pd.read_csv(chunk_file_path, low_memory=False)
    if chunk_df.empty:
        return result_df
    
    chunk_df = chunk_df[chunk_df.isin(methods_set).any(axis=1)]

    total_count = 0
    total_count_direct = 0
    # Iterate over the benchmark names
    for benchmark in project_benchmarks:

        # Filter main dataframe for the current benchmark name
        benchmark_data = chunk_df[chunk_df.iloc[:, 0] == benchmark]
        
        #Adding a marker to the start of the row before flattening the Row
        benchmark_data['row_start'] = '#'

        # Get the methods from the other columns (excluding the first column)
        methods = benchmark_data.iloc[:, 1:].values.flatten()
        flatten_set = set(methods)

        # Filter the methods based on the project's methods
        # matched_methods = set(method for method in methods if method in methods_set)
        matched_methods = flatten_set.intersection(methods_set)
        direct_called_methods = get_direct_calls_set(methods, methods_set)

        # Count the matched methods
        count = len(matched_methods)

        # Count Direct matched methods
        count_direct = len(direct_called_methods)

        total_count += count
        total_count_direct += count_direct

        # Append the results to the result list
        result_list.append({'Project Name': project_name,
                            'Benchmark Name': benchmark,
                            'Count': count, 
                            'Direct Count':count_direct,
                            'Methods': ','.join(matched_methods),
                            'Direct Methods': ','.join(direct_called_methods)})
    
    result_df = pd.DataFrame(result_list)
    return result_df

# %%
def process_project(project_name, benchmark_df, method_df, truncated_csvs_path, output_folder):

    # Filter method dataframe for the given project name
    project_methods = method_df[method_df['project_name'] == project_name]['method']
    methods_set = set(project_methods.values)

    # Filter benchmark dataframe for the benchmark names corresponding to the project
    project_benchmarks = benchmark_df[benchmark_df['project'] == project_name]['benchmark']
    
    # Path to the project input chunks directory
    project_chunk_directory = os.path.join(truncated_csvs_path, project_name)
    
    # Iterate over the CSV files in the project chunks directory
    for file_name in os.listdir(project_chunk_directory):
        chunk_file_path = os.path.join(project_chunk_directory, file_name)
        chunk_no = chunk_file_path.split('_')[-1].split('.')[0]
        
        result_df = process_chunk(project_name, chunk_file_path, project_benchmarks, methods_set)   
        
        if not result_df.empty:
            results_csv_path = os.path.join(output_folder, f"{project_name}_Results_Chunk_{chunk_no}.csv")
            result_df.to_csv(results_csv_path, index=False)


# %%
#Main execution of the Script Starts here
#CREATING THE PROCESSED CHUNKS AND STORING EACH CHUNK IN A SEPARATE CSV
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--truncated_csvs_path', type=str, required=True,
                        help='Directory containing truncated CSV files from the 0D_Chunks_Truncated script.')
    parser.add_argument('--output_folder_b2m', type=str, required=True,
                        help='Output directory to store Benchmark to Method analysis results.')
    parser.add_argument('--output_folder_m2b', type=str, required=True,
                        help='Output directory to store Method to Benchmark analysis results.')
    parser.add_argument('--benchmarks_csv_path', type=str, required=True,
                        help='Path to the list of benchmarks CSV file')
    parser.add_argument('--methods_csv_path', type=str, required=True,
                        help='Path to the methods CSV file from the 0B_Methods_to_CSV script, listing methods to analyze.')
    parser.add_argument('--shortlisted_projects_csv', type=str, required=True,
                        help='Path to the CSV file listing the selected projects for analysis.')

    args = parser.parse_args()

    # Load benchmarks and methods dataframes
    benchmark_df = pd.read_csv(args.benchmarks_csv_path)
    method_df = pd.read_csv(args.methods_csv_path)
    project_names = pd.read_csv(args.shortlisted_projects_csv)["Project"]

    for project in project_names:
        print(f"Processing {project}...")

        # Define output paths for both types of analysis
        output_path_b2m = os.path.join(args.output_folder_b2m, project)
        output_path_m2b = os.path.join(args.output_folder_m2b, project)
        create_directory_if_not_exists(output_path_b2m)
        create_directory_if_not_exists(output_path_m2b)
        
        # Process each project using the truncated chunks
        process_project(project, benchmark_df, method_df, args.truncated_csvs_path, output_path_b2m)

    # Iterate over projects for aggregation and analysis
    for project in project_names:
        print(f"Aggregating and analyzing data for project: {project}")
        aggregated_df = aggregate_output(project, args.output_folder_b2m)
        methods_dict, direct_methods_dict = create_method_dictionaries(aggregated_df)
        project_methods = method_df[method_df['project_name'] == project]['method']
        methods_set = set(project_methods.values)
        methods_to_benchmarks_analysis(project, methods_set, methods_dict, direct_methods_dict, args.output_folder_m2b)
    
    # Combine and summarize CSVs for Method to Benchmark and Benchmark to Method analyses
    combined_methods_to_bench_csv = os.path.join(args.output_folder_m2b, "00_combined_methods_to_bench.csv")
    combine_csv_files(args.output_folder_m2b, combined_methods_to_bench_csv)
    
    combined_bench_to_methods_csv = os.path.join(args.output_folder_b2m, "00_combined_bench_to_methods.csv")
    combine_csv_files(args.output_folder_b2m, combined_bench_to_methods_csv)
    
    # Creating summary CSVs
    # This part assumes you have the required data loaded into 'df' for each summary
    # Replace 'df' with actual DataFrame loading lines if needed
    df_methods_to_bench = pd.read_csv(combined_methods_to_bench_csv)
    df_bench_to_methods = pd.read_csv(combined_bench_to_methods_csv)

    # Summarizing Method to Benchmarks
    summary_methods_to_bench = df_methods_to_bench.groupby('Project Name').agg({
        'Method': 'size', 'is_Benchmarked': 'sum', 'is_Directly_Benchmarked': 'sum', 'Benchmark_Count': 'sum', 'Direct_Benchmark_Count': 'sum'
    }).reset_index()
    summary_methods_to_bench.to_csv(os.path.join(args.output_folder_m2b, "00_combined_methods_to_bench_summary.csv"), index=False)
    
    # Summarizing Benchmarks to Methods
    summary_bench_to_methods = df_bench_to_methods.groupby('Project Name').agg({
        'Benchmark Name': 'size', 'Count': 'sum', 'Direct Count': 'sum'
    }).reset_index()
    summary_bench_to_methods.to_csv(os.path.join(args.output_folder_b2m, "00_combined_bench_to_methods_summary.csv"), index=False)