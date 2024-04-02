import os
import csv
from lxml import etree as let
import pandas as pd
import re
import argparse
from glob import glob

# Command line arguments
parser = argparse.ArgumentParser(description="Extract Java method signatures to CSV files.")
parser.add_argument('--srcml_dir', type=str, required=True, help='Path to the folder containing srcML files.')
parser.add_argument('--csv_target_path', type=str, required=True, help='Target path to save the CSV files.')
args = parser.parse_args()

# Update paths using command line arguments
srcml_folder_path = args.srcml_dir
csv_target_path = args.csv_target_path

# srcML Namespace 
srcml_namespace = {"srcml": "http://www.srcML.org/srcML/src"}

# Stack class for Utility usage
class Stack:
    def __init__(self):
        self.items = []
        
    def is_empty(self):
        return not self.items
      
    def push(self, item):
        self.items.append(item)
        
    def pop(self):
        if self.items:
            return self.items.pop()
        else:
            return None
          
    def peek(self):
        if self.items:
            return self.items[-1]
        else:
            return None
          
    def size(self):
        return len(self.items)
      
    def __str__(self):
        return str(self.items)

# Other function definitions to get the methods from the srcML file
def get_filtered_methods(srcml_file, isBenchTagged, srcml_namespace):
    ltree = let.parse(srcml_file)
    lroot = ltree.getroot()
    functions_query = "//srcml:function"
    function_nodes = lroot.xpath(functions_query, namespaces=srcml_namespace)
    functions = []
    for node in function_nodes:
        functions.append(node)
    return functions

def extract_method_names(functions):
    function_names = []
    for function in functions:
        name_stack = Stack()
        package_name = "".join(function.xpath(".//ancestor::srcml:class/preceding-sibling::srcml:package/srcml:name//text()", namespaces=srcml_namespace))
        current_name = "".join(function.xpath("srcml:name/text()", namespaces=srcml_namespace))
        name_stack.push(current_name)
        function_names.append(package_name + "." + current_name)
    return function_names

def parse_srcml_file(srcml_file):
    functions = get_filtered_methods(srcml_file, False, srcml_namespace)
    methods = extract_method_names(functions)
    return methods

def create_project_csv_pd(project_name, methods, csv_target_path):
    df = pd.DataFrame(methods, columns=['Method_name'])
    df['project_name'] = project_name
    csv_file = os.path.join(csv_target_path, f"{project_name}.csv")
    df.to_csv(csv_file, index=False, encoding='utf-8')

def process_projects(srcml_folder_path, csv_target_path):
    srcml_files = [os.path.join(srcml_folder_path, f) for f in os.listdir(srcml_folder_path) if f.endswith('.xml')]
    for srcml_file in srcml_files:
        project_name = os.path.splitext(os.path.basename(srcml_file))[0]
        methods = parse_srcml_file(srcml_file)
        create_project_csv_pd(project_name, methods, csv_target_path)

if __name__ == "__main__":
    process_projects(srcml_folder_path, csv_target_path)
