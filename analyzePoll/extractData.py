"""
Preamble: 
This script is designed to extract data from a XLSX (excel) file and parse the data out and either turn it into a JSON file / vector / string etc for further analysis.
"""
# import all the correct libraries

import pandas as pd


# Function to extract data from a specific column in an Excel file
def extract_column_data(file_path, column_name, skiprowcount=0):
    """Extract data from a specific column in an Excel file. (Skip the first rows according to what data is being extracted)""" 
    df = pd.read_excel(file_path, header=0)  # Load the Excel file with the first row as header
    if column_name in df.columns:
        # skiprowcount = 8 is all the data AFTER the first 8 rows (aka the survey update)
        return df[column_name].dropna().tolist()[skiprowcount:]  # Return non-null values as a list
    else:
        return f"Column '{column_name}' not found."
    
file_path = "CunyMetroCard191.xlsx"
column_name = """What is your starting station for your trip to Hunter? (None if you don't use the train)
"""

#data = extract_column_data(file_path, column_name, skiprowcount=0)
#print(data)