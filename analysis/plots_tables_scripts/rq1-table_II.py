# %%
import pandas as pd

# %%
plots_path = "../../figures"
tables_path = "../../tables"

u2m_path = "../../inputs/wrangled/u2m/00_combined_test_to_methods_summary.csv"
b2m_path = "../../inputs/wrangled/b2m/00_combined_bench_to_methods_summary.csv"
metainfo_path = "../../inputs/Project_Meta_Info.csv"
methods_summary_path = "../../inputs/methods/00_summary.csv"

df_u2m_summary = pd.read_csv(u2m_path)
df_b2m_summary = pd.read_csv(b2m_path)

df_github_metadata = pd.read_csv(metainfo_path, delimiter='\t')
df_summary_methods = pd.read_csv(methods_summary_path)


# %%
# Rename the columns for merging
df_b2m_summary = df_b2m_summary.rename(columns={"Project Name": "Project", "Total Benchmarks": "Benchmarks(Total)"})
df_u2m_summary = df_u2m_summary.rename(columns={"Project Name": "Project", "Total Tests": "Unit Tests(Total)"})
df_summary_methods = df_summary_methods.rename(columns={"project_name": "Project", "method_count": "Methods(Total)"})
df_github_metadata = df_github_metadata.rename(columns={"Project Name": "Project", "Stars":"GitHub Stars"})

# Drop extra columns before merging
df_b2m_summary = df_b2m_summary.drop(columns=['Methods Benchmarked', 'Methods Directly Benchmarked'])
df_u2m_summary = df_u2m_summary.drop(columns=['Methods Tested', 'Methods Directly Tested'])
df_github_metadata = df_github_metadata.drop(columns=['Contributors', 'Forks', 'Releases'])

# Merge the dataframes using Left Join only
df_merged = pd.merge(df_b2m_summary, df_u2m_summary, on="Project", how="left")
df_final = pd.merge(df_merged, df_summary_methods, on="Project", how="left")

df_github_metadata['Project'] = df_github_metadata['Project'].str.strip()
df_github_metadata['Project'] = df_github_metadata['Project'].str.replace(r'\\_', '_', regex=True)

df_final = pd.merge(df_final, df_github_metadata, on="Project", how="left")

# Replace NaNs with "*"
df_final.fillna("-", inplace=True)

# Reorder the columns
df_final = df_final[['Project','GitHub Stars', 'Methods(Total)', 'Benchmarks(Total)', 'Unit Tests(Total)']]
df_final['Unit Tests(Total)'] = df_final['Unit Tests(Total)'].apply(lambda x: int(x) if str(x).replace('.', '', 1).isdigit() else x)

# Sort the dataframe by 'Project' in a case-insensitive manner
df_final = df_final.sort_values(by='Project', key=lambda col: col.str.lower()).reset_index(drop=True)

# Display the final dataframe
df_final

# %%
from tabulate import tabulate
import subprocess
import os
def save_df_as_pdf(df, pdf_filename, keep_tex=False):
    # Convert the DataFrame to a LaTeX table
    latex_table = tabulate(df, tablefmt='latex_booktabs', headers='keys', showindex=False)

    # Create a standalone LaTeX document with the table
    latex_doc = f"""\\documentclass[preview]{{standalone}}
    \\usepackage{{booktabs}}

    \\begin{{document}}
    {latex_table}
    \\end{{document}}
    """

    # Get the file path, file name (excluding extension), and the .tex file name
    file_path, file_name_ext = os.path.split(pdf_filename)
    file_name, _ = os.path.splitext(file_name_ext)
    tex_filename = os.path.join(file_path, f'{file_name}.tex')

    # Save the document to a .tex file
    with open(tex_filename, 'w') as f:
        f.write(latex_doc)

    # Compile the LaTeX document into a PDF file using pdflatex
    subprocess.run(['pdflatex', '-output-directory', file_path, tex_filename])

    # Clean up intermediate files
    if not keep_tex:
        os.remove(tex_filename)
    os.remove(os.path.join(file_path, f'{file_name}.log'))
    os.remove(os.path.join(file_path, f'{file_name}.aux'))


# %%
save_df_as_pdf(df_final, os.path.join(tables_path, 'tbl_Raw_Data_Stats.pdf'), True)


