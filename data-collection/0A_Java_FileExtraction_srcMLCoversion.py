import os
import shutil
import subprocess
import threading
from fnmatch import fnmatch
import argparse

def extract_java_files(project_path, extraction_dir, extraction_pattern):
    project_name = os.path.basename(project_path)
    new_project_dir = os.path.join(extraction_dir, project_name)
    if not os.path.exists(new_project_dir):
        os.makedirs(new_project_dir)
    
    for path, _, files in os.walk(project_path):
        for name in files:
            if fnmatch(name, extraction_pattern):
                source = os.path.join(path, name)
                destination = os.path.join(new_project_dir, name)
                shutil.copy(source, destination)

def convert_to_srcml(source_dir, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    
    for subdir in os.listdir(source_dir):
        input_dir = os.path.join(source_dir, subdir)
        output_file = os.path.join(target_dir, f"{subdir}.xml")
        with open(output_file, 'w+') as f:
            subprocess.run(['srcml', input_dir, '-o', output_file], stdout=f)

def main(args):
    projects_path_list = [f.path for f in os.scandir(args.source_projects_path) if f.is_dir()]
    
    threads = [
        threading.Thread(target=extract_java_files, args=(project_path, args.extraction_dir, "*.java"))
        for project_path in projects_path_list
    ]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    convert_to_srcml(args.extraction_dir, args.srcml_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process and convert Java projects to srcML format.')
    parser.add_argument('--source_projects_path', type=str, required=True, help='Source repositories directory path')
    parser.add_argument('--extraction_dir', type=str, required=True, help='Path(Temporary) to extract all Java files from a project')
    parser.add_argument('--srcml_dir', type=str, required=True, help='Path for storing srcML files for all projects')
    
    args = parser.parse_args()
    main(args)
