import os
import pandas as pd
from collections import deque
import argparse

def create_directory_if_not_exists(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def process_lines_in_chunks(file_path, chunk_size):
    with open(file_path, 'r') as file:
        current_chunk = deque()
        for line in file:
            current_chunk.append(line.strip().split(';'))
            if len(current_chunk) == chunk_size:
                yield list(current_chunk)
                current_chunk.clear()
        if current_chunk:
            yield list(current_chunk)

def process_project(project, input_directory, output_directory, chunk_size):
    file_path = os.path.join(input_directory, f"{project}.folded")
    chunk_output_directory = os.path.join(output_directory, project)
    create_directory_if_not_exists(chunk_output_directory)
    
    print(f"Processing project {project}")
    for chunk_index, chunk in enumerate(process_lines_in_chunks(file_path, chunk_size)):
        df_chunk = pd.DataFrame(chunk)
        df_chunk.columns = [f"call_{i}" for i in range(1, len(df_chunk.columns) + 1)]
        df_chunk = df_chunk.where(pd.notnull(df_chunk), None)
        chunk_file_name = f"{project}_chunk_{chunk_index}.csv"
        chunk_file_path = os.path.join(chunk_output_directory, chunk_file_name)
        df_chunk.to_csv(chunk_file_path, index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Split folded files into chunks and process them into CSV files.")
    parser.add_argument('--callstacks_input_directory', type=str, required=True, help='Directory containing call stacks.')
    parser.add_argument('--shorlisted_projects_csv', type=str, required=True, help='List of project names to process.')
    parser.add_argument('--output_directory', type=str, required=True, help='Directory to save the output chunks.')
    parser.add_argument('--chunk_size', type=int, default=20000, help='Number of call stacks per chunk.Default is 20000.')
    
    args = parser.parse_args()
    
    project_list = pd.read_csv(args.shorlisted_projects_csv)["Project"]
    for project in project_list:
        process_project(project, args.callstacks_input_directory, args.output_directory, args.chunk_size)
