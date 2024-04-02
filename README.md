
# An Empirical Study on Performance Test Coverage: Replication Package

This repository contains the replication package for the paper "*An Empirical Study on Performance Test Coverage*". It includes all necessary scripts and instructions to replicate the experiments and analyses presented in the paper.

## Requirements

- Python 3.10.5
- [Additional dependencies are listed in the `requirements.txt` file](requirements.txt)

Use the following commands to install Python dependencies:
```
pip install --upgrade pip
pip install -r requirements.txt
```

## Directory Structure and Descriptions

- A comprehensive guide providing all necessary instructions and descriptions to understand and replicate the analyses.


### Data Collection Instructions
In order to collect the callstacks that will be used to determine the coverage of methods, we leverage [async-profiler](https://github.com/async-profiler/async-profiler).

Specifically, given a [self-contained executable JAR of JMH](https://github.com/openjdk/jmh) `benchmarks.jar`, we run the following command to collect the methods invoked by each benchmark:

```
java -jar benchmarks.jar -bm avgt -wi 0 -i 1 -f 1 -r 100ms -foe false -jvmArgsPrepend "-agentpath:{ASYNC_PROFILER_PATH}/build/libasyncProfiler.so=start,event=cpu,collapsed,cstack=no,include=*jmh*,file=.%t.folded,interval=1"
``````

Similarly, for JUnit we run:

```
mvn test -DargLine="-agentpath:{ASYNC_PROFILER_PATH}/build/libasyncProfiler.so=start,event=cpu,collapsed,cstack=no,include=*junit*,file=.%t.folded,interval=1"
```
### Collecting Methods
To  extract the list of Java method signatures that appear in the projects, we used [srcML toolkit](https://www.srcml.org/). We extracted all the Java files and converted them to srcML format using the script `0A_Java_FileExtraction_srcMLCoversion.py`. To run the `0A_Java_FileExtraction_srcMLConversion.py` script, specify three command-line arguments:
1. `--source_projects_path`: The path to the directory containing the source projects from which Java files will be extracted.
2. `--extraction_dir`: The path to the directory where all extracted Java files will be stored temporarily.
3. `--srcml_dir`: The path to the directory where the srcML files for all projects will be generated.
4. `--csv_target_path`: The path to store the csv for list of Java method signatures

The `0A_Java_FileExtraction_srcMLConversion.py` can be run as:

```
python 0A_Java_FileExtraction_srcMLConversion.py --source_projects_path "/path/to/source/projects" --extraction_dir "/path/to/extraction/dir" --srcml_dir "/path/to/srcml/dir"
```

The generated srcML files can be used to extract the list of Java method signatures using `0B_Methods_to_CSV.py`. It can be run as:
```
python 0B_Methods_to_CSV.py --srcml_dir "/path/to/srcml/files" --csv_target_path "/path/to/csv/output"
```

### Preprocessing the Call Stacks
The collected call stacks are preprocessed using the following scripts. Run these scripts in sequence to generate the preprocessed data for further analysis.

1. `0C_Folded_to_Chunks.py`: splits folded files into specified chunk sizes and processes them into CSV format. This script uses the following command-line arguments:
```
python 0C_Folded_to_Chunks.py --folded_input_directory "/path/to/folded/files" --shorlisted_projects_csv "/path/to/projects_list.csv" --output_directory "/path/to/output/chunks" --chunk_size 20000
```
2. `0D_Chunks_Truncated.py`: filters and truncates the processed chunks to focus on relevant call stacks. Use the following command-line arguments to run this script:

```
python 0D_Chunks_Truncated.py --chunks_directory "/path/to/processed/chunks" --benchmarks_csv_path "/path/to/benchmarks.csv" --shortlisted_projects_csv "/path/to/projects_list.csv"
```
3. `0E_Chunks_Analysed.py`: analyzes the preprocessed chunks for coverage of methods by the benchmarks. Use the following command-line arguments to run this script:

```
python 0E_Chunks_Analysed.py --truncated_csvs_path "/path/to/truncated/csvs" --output_folder_b2m "/path/to/output/benchmark_to_method" --output_folder_m2b "/path/to/output/method_to_benchmark" --benchmarks_csv_path "/path/to/benchmarks.csv" --methods_csv_path "/path/to/methods.csv" --shortlisted_projects_csv "/path/to/shortlisted/projects.csv"
```

### analysis/
Scripts in this directory perform overlap and test coverages analysis.
- `1-Overlap-JMH.py`
- `2-Overlap-JUnit.py`
- `3-Coverage-JMH.py`
- `4-Coverage-JUnit.py`
   - Run these scripts in sequence to generate intermediate outputs for further analyses and to answer research questions 1 and 2.

### analysis/plots_tables_scripts/
Scripts for generating plots and tables related to the research questions.
- Run these scripts after executing the main analysis scripts (`1-Overlap-JMH.py`, `2-Overlap-JUnit.py`, `3-Coverage-JMH.py`, `4-Coverage-JUnit.py`).

### figures/
Contains output figures from the analysis scripts. Each figure is related to specific research questions, as indicated in the filenames.

### inputs/
Contains all necessary input data for performing test overlap and coverage analysis.
- `Project_Meta_Info.csv`: Metadata including GitHub stars information for each project.
- Subdirectories such as `benchmarks/`, `methods/`, and `unit_tests/` contain collected data used in the analysis.

### outputs/
Contains intermediate outputs generated by the main analysis scripts (`1-Overlap-JMH.py`, `2-Overlap-JUnit.py`, `3-Coverage-JMH.py`, `4-Coverage-JUnit.py`).

### tables/
Contains generated tables as outputs from the analysis scripts.

## Execution Instructions

1. **Running Analysis Scripts:**
   - Navigate to the `analysis/` directory.
   - Run the scripts in sequence:
     ```
     python 1-Overlap-JMH.py
     python 2-Overlap-JUnit.py
     python 3-Coverage-JMH.py
     python 4-Coverage-JUnit.py
     ```

2. **Generating Plots and Tables:**
   - Navigate to the `analysis/plots_tables_scripts/` directory.
   - Run the scripts to generate plots and tables. Below are the commands to execute each script:
   ```bash
   python rq1-fig3.py
   python rq1-fig4.py
   python rq1-fig5.py
   python rq1-table_II.py
   python rq2-fig6.py
   python rq2-fig7.py
   python rq2-fig8.py
   python rq2-fig9.py
   python rq3-fig10.py
   python rq3-fig11.py
   python rq4-fig12.py
   python rq4-fig13.py
   ```

3. **Viewing Results:**
   - Check the `figures/` and `tables/` directories for output figures and tables.
   - Intermediate results can be found in the `outputs/` directory.
