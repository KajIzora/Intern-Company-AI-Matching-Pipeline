import pandas as pd
import numpy as np
import openpyxl
from prettytable import PrettyTable
from IPython.display import display, HTML
import sys
import os
from tqdm import tqdm
from pandas.io.formats.excel import ExcelFormatter
import json



def read_excel_custom(file_path):
    # Define a function to load Excel files with specific NA handling
    return pd.read_excel(
        file_path,
        keep_default_na=False,  # Do not automatically consider the default strings as missing values
        na_values=['']  # Define what should be considered a missing value
    )


def read_csv_custom(file_path, delimiter, dtype_spec=None):
    """
    Loads a CSV file with specific NA handling and optional dtype specifications.
    
    Args:
    - file_path (str): Path to the CSV file.
    - delimiter (str): Delimiter used in the CSV file.
    - dtype_spec (dict, optional): Dictionary specifying data types for certain columns.
    
    Returns:
    - DataFrame: A pd DataFrame containing the data from the CSV file.
    """
    return pd.read_csv(
        file_path,
        sep=delimiter,  # Set the delimiter for the file
        keep_default_na=False,  # Do not automatically consider the default NA values
        na_values=[''],  # Treat empty strings as NA values
        dtype=dtype_spec  # Apply data types to specified columns if provided
    )


''' 
This function is for better table visualization in Jupyter Notebook.
'''
# Function to print DataFrame as pretty table including the DataFrame index
def pretty_print(df):
    # Check if the input is a Series and convert it to a DataFrame if necessary
    if isinstance(df, pd.Series):
        df = df.to_frame()

    # Create a PrettyTable object
    table = PrettyTable()

    # Adding 'Index' as the first field name
    table.field_names = ['Index'] + df.columns.tolist()

    # Add rows to the table including the index
    for index, row in df.iterrows():
        # Combine the index and the row into one list
        table.add_row([index] + row.tolist())

    # Print the table
    print(table)



# Save the DataFrame
def save_df(df, base_path, file_name, formats):
    """
    Saves a DataFrame in specified formats with checks for CSV compatibility.

    Args:
        df (DataFrame): The DataFrame to save.
        base_path (str): The base directory for saving files.
        file_name (str): The base name of the file without extension.
        formats (list): List of formats to save the DataFrame ('excel', 'csv', 'parquet').
        chunk_size (int): Number of rows to write per chunk for progress bar (default is 1000).

    Returns:
        None
    """
    # Define paths for each format
    paths = {
        'excel': os.path.join(base_path, 'excel_files', f'{file_name}.xlsx'),
        'csv': os.path.join(base_path, 'csv_files', f'{file_name}.csv'),
        'parquet': os.path.join(base_path, 'parquet_files', f'{file_name}.parquet')
    }

    # Save as Excel with progress bar
    # Save as Excel
    if 'excel' in formats:
        with pd.ExcelWriter(paths['excel']) as writer:
            df.to_excel(writer, index=False)
        print("Excel file saved.")

    # Save as CSV with delimiter check
    if 'csv' in formats:
        df_str = df.astype(str)
        
        # Check if the DataFrame contains '|' characters
        if df_str.stack().apply(lambda x: '|' in x).any():
            user_input = input("The DataFrame contains '|' characters. Replace all '|' with ';'? [y/n]: ")
            if user_input.lower() == 'y':
                df_str.replace({'|': ';'}, regex=True, inplace=True)
                df_str.to_csv(paths['csv'], index=False, sep='|')
                print("CSV file saved after replacing '|' with ';'.")
            elif user_input.lower() == 'n':
                print("Cannot save to CSV using '|' as a delimiter because '|' characters are present in the DataFrame.")
                return
            else:
                print("Invalid input. Exiting without saving CSV.")
                return
        else:
            df.to_csv(paths['csv'], index=False, sep='|')
            print("CSV file saved.")

    # Save as Parquet
    if 'parquet' in formats:
        df.to_parquet(paths['parquet'])
        print("Parquet file saved.")

def load_df(base_path, file_name):
    """
    Loads a DataFrame from a parquet file given a base path and file name.

    Args:
        base_path (str): The base directory where the parquet files are stored.
        file_name (str): The name of the parquet file to load.

    Returns:
        DataFrame: The loaded DataFrame.
    """
    full_path = os.path.join(base_path, 'parquet_files', f'{file_name}.parquet')
    return pd.read_parquet(full_path)


def as_list(info):
    return [line.strip() for line in info.strip().split('\n') if line.strip()]



def cols(df ,path):
    path = path
    # Open the file in write mode
    with open(path, 'w') as f:
        # Iterate through the DataFrame columns and write each one to a new line in the file
        for col in df.columns:
            f.write(f'{col}\n')


import pandas as pd

def print_csv(df, columns, delimiter='|', num_rows=10):
    """
    Prints the specified columns of the DataFrame in CSV format with the specified delimiter.

    Parameters:
    df (pandas.DataFrame): The DataFrame to print.
    columns (list): The list of column names to include in the output.
    delimiter (str): The delimiter to use in the CSV format (default is '|').
    num_rows (int): The number of rows to print (default is None, which prints all rows).
    """
    # Select the specified columns
    selected_columns = df[columns]
    
    # If num_rows is specified, select only the top rows
    if num_rows is not None:
        selected_columns = selected_columns.head(num_rows)
    
    # Convert to CSV format and print
    csv_output = selected_columns.to_csv(index=False, sep=delimiter)
    print(csv_output)
    

# function for loading project path
def load_project_path(filename='project_config.json'):
    try:
        with open(filename, 'r') as f:
            config = json.load(f)
        return config['path_to_project']
    except FileNotFoundError:
        print(f"Configuration file {filename} not found.")
        return None
    
# function for saving project path
def save_project_path(path_to_project, filename='project_config.json'):
    config = {'path_to_project': path_to_project}
    with open(filename, 'w') as f:
        json.dump(config, f)
    print(f"Project path saved to {filename}.")
    


def save_html_table(df, save_path, title=""):
    """
    Saves a DataFrame as an HTML table with customized formatting and an optional title.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing the data.
    save_path (str): The file path where the HTML file will be saved.
    title (str): The title of the table to be displayed above it.

    Returns:
    None
    """
    # Convert the DataFrame to an HTML table
    html = df.to_html(index=False, classes='table table-striped', border=2)

    # Replace newline characters with <br> tags in the HTML
    html = html.replace('\\n', '<br>')

    # Customize the HTML to make grid lines thicker, apply a blue color to the headers, and align text to the top and left
    html = html.replace('<table', '<table style="border-collapse: collapse; width: 100%; border: 2px solid black;"')
    html = html.replace('<thead>', '<thead style="background-color: paleturquoise; text-align: left;">')
    html = html.replace('<th style="text-align: right;', '<th style="text-align: left; padding: 10px; border: 2px solid black;"')  # Ensure header text aligns left
    html = html.replace('<th>', '<th style="text-align: left; padding: 10px; border: 2px solid black;">')  # Ensure header text aligns left
    html = html.replace('<td>', '<td style="vertical-align: top; padding: 10px; border: 2px solid black;">')

    # Add title to the HTML if provided
    if title:
        html = f"<h2 style='text-align: center;'>{title}</h2>" + html

    # Save the customized HTML
    with open(save_path, 'w') as f:
        f.write(html)
