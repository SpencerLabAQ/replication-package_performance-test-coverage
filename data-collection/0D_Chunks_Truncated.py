import os
import pandas as pd
import re
import argparse

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def truncate_row_before_match(row, pattern_to_benchmark):
    for idx, cell in enumerate(row):
        matching_benchmark = next((pattern_to_benchmark[compiled_pattern] for compiled_pattern in pattern_to_benchmark.keys() if compiled_pattern.search(str(cell))), None)
        if matching_benchmark:
            values = [matching_benchmark] + row[idx:].tolist()
            if idx == 0:
                values.pop()
            values += [None] * (len(row) - len(values))
            truncated_row = pd.Series(values, index=row.index)
            return truncated_row
    return row

def filter_and_truncate_chunks_faster(project, chunks_directory, pattern_to_benchmark):
    input_project_directory = os.path.join(chunks_directory, project)
    output_truncated_directory = os.path.join(chunks_directory, 'Truncated', project)
    create_directory_if_not_exists(output_truncated_directory)

    for chunk_file in os.listdir(input_project_directory):
        chunk_file_path = os.path.join(input_project_directory, chunk_file)
        chunk_df = pd.read_csv(chunk_file_path, dtype=object)
        filtered_df = chunk_df[chunk_df.apply(lambda row: any(compiled_pattern.search(str(cell)) for cell in row for compiled_pattern in pattern_to_benchmark), axis=1)]
        truncated_df = filtered_df.apply(lambda row: truncate_row_before_match(row, pattern_to_benchmark), axis=1)
        output_file_name = f"Truncated_{chunk_file}"
        output_file_path = os.path.join(output_truncated_directory, output_file_name)
        truncated_df.to_csv(output_file_path, index=False)
        print(f"Finished filtering and truncation for chunk: {chunk_file}")

def extract_benchmark_components_re(benchmark):
    pattern = re.compile(r"^(\w+(?:\.\w+)*)\.(\w+)\.(\w+)$")
    match = pattern.match(benchmark)
    if match:
        package_name = match.group(1)
        class_name = match.group(2)
        bench_name = match.group(3)
        return package_name, class_name, bench_name
    else:
        return None, None, None
    
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filters and truncates chunks based on benchmarks.")
    parser.add_argument('--chunks_directory', type=str, required=True, help='Directory containing chunk files.')
    parser.add_argument('--benchmarks_csv_path', type=str, required=True, help='CSV file containing benchmark information.')
    parser.add_argument('--shortlisted_projects_csv', type=str, required=True, help='CSV file listing projects to process.')

    args = parser.parse_args()

    benchmarks_df = pd.read_csv(args.benchmarks_csv_path)
    project_list = pd.read_csv(args.shortlisted_projects_csv)["Project"]

    for project in project_list:
        print(f"Processing {project}...")
        benchmarks_set = set(benchmarks_df.query('project == @project')["benchmark"])
        pattern_to_benchmark = {}
        for bench in benchmarks_set:
            pkg, clss, meth = extract_benchmark_components_re(bench)
            pkg = re.escape(pkg)
            clss = re.escape(clss)
            meth = re.escape(meth)
            pattern = f"{pkg}\.?.*{clss}\.?.*{meth}"
            compiled_pattern = re.compile(pattern)
            pattern_to_benchmark[compiled_pattern] = bench

        filter_and_truncate_chunks_faster(project, args.chunks_directory, pattern_to_benchmark)
