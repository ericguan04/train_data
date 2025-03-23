#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fair Fares Analysis Script

This script analyzes data from the CUNY MetroCard survey to understand
the awareness, application rates, acceptance rates, and financial impact
of the Fair Fares NYC program among survey respondents.
"""

import pandas as pd
import os

# -----------------------------------------------------------------------------
# CONFIGURATION AND SETUP
# -----------------------------------------------------------------------------

# Define the path to the Excel file
excel_file = 'CunyMetroCard191.xlsx'

# Check if the file exists
if not os.path.exists(excel_file):
    print(f"Error: The file '{excel_file}' does not exist in the current directory.")
    print(f"Current working directory: {os.getcwd()}")
    print("Please make sure the file is in the correct location.")
    exit(1)

# -----------------------------------------------------------------------------
# INITIAL DATA EXPLORATION
# -----------------------------------------------------------------------------

try:
    # Try different approaches to read the Excel file
    # First, try reading without skipping rows to see the structure
    print(f"Reading data from {excel_file}...")
    df_preview = pd.read_excel(excel_file, nrows=15)
    
    # Print column names to help debug
    print("\nPreview of columns in the Excel file:")
    for i, col in enumerate(df_preview.columns):
        print(f"{i}: {col}")
    
    # Now read the file with skipping 8 rows as requested
    df = pd.read_excel(excel_file, skiprows=8)
    
    # Try to find the Fair Fares awareness column
    # First, look for column with index 28 (which is the 29th column, matching the report)
    if len(df.columns) > 28:
        # Get the 29th column (index 28)
        awareness_column = df.columns[28]
        print(f"\nUsing column at index 28: {awareness_column}")
        
        # Count responses
        value_counts = df[awareness_column].value_counts(dropna=False)
        total_responses = sum(value_counts)
        
        print(f"Total number of responses: {total_responses}")
        
        # Print individual counts and calculate percentages
        print("\nResponse counts and percentages:")
        for value, count in value_counts.items():
            value_str = str(value) if not pd.isna(value) else "No response"
            percentage = (count / total_responses) * 100
            print(f"{value_str}: {count} ({percentage:.2f}%)")
    else:
        print("\nCould not find the Fair Fares awareness column (index 28).")
        print("Available columns:")
        for i, col in enumerate(df.columns):
            print(f"{i}: {col}")

except Exception as e:
    print(f"Error: {e}")


# -----------------------------------------------------------------------------
# ANALYSIS FUNCTIONS
# -----------------------------------------------------------------------------

def analyze_fair_fares_application():
    """
    Analyzes how many people who were aware of Fair Fares actually applied for it.
    
    This function filters the dataset to include only respondents who were aware of
    the Fair Fares program, then calculates how many of those respondents actually
    applied for the program.
    """
    try:
        print("\n=== ANALYZING FAIR FARES APPLICATION RATES ===\n")
        print("Analyzing how many people who were aware of Fair Fares actually applied for it...")
        
        # Check if the file exists
        if not os.path.exists(excel_file):
            print(f"Error: The file '{excel_file}' does not exist in the current directory.")
            print(f"Current working directory: {os.getcwd()}")
            print("Please make sure the file is in the correct location.")
            return
        
        # Read the Excel file with skipping 8 rows as before
        df = pd.read_excel(excel_file, skiprows=8)
        
        # Get the awareness column (index 28, which is the 29th column)
        if len(df.columns) <= 28:
            print("Could not find the Fair Fares awareness column (index 28).")
            return
            
        awareness_column = df.columns[28]
        
        # Get the application column (index 29, which is the 30th column)
        if len(df.columns) <= 29:
            print("Could not find the Fair Fares application column (index 29).")
            return
            
        application_column = df.columns[29]
        
        print(f"Using awareness column at index 28: {awareness_column}")
        print(f"Using application column at index 29: {application_column}")
        
        # Filter for people who were aware of Fair Fares (answered 'Yes')
        aware_people = df[df[awareness_column] == 'Yes']
        total_aware = len(aware_people)
        
        if total_aware == 0:
            print("No respondents were aware of Fair Fares.")
            return
            
        print(f"\nTotal number of people aware of Fair Fares: {total_aware}")
        
        # Count how many of those aware people applied for Fair Fares
        application_counts = aware_people[application_column].value_counts(dropna=False)
        
        # Print individual counts and calculate percentages
        print("\nApplication rates among those aware of Fair Fares:")
        for value, count in application_counts.items():
            value_str = str(value) if not pd.isna(value) else "No response"
            percentage = (count / total_aware) * 100
            print(f"{value_str}: {count} ({percentage:.2f}%)")
            
    except Exception as e:
        print(f"Error in analyze_fair_fares_application: {e}")


def analyze_fair_fares_acceptance():
    """
    Analyzes how many Fair Fares applications were accepted or rejected.
    
    This function filters the dataset to include only respondents who applied for
    the Fair Fares program, then calculates the acceptance and rejection rates
    among those applicants.
    """
    try:
        print("\n=== ANALYZING FAIR FARES ACCEPTANCE RATES ===\n")
        print("Analyzing how many Fair Fares applications were accepted or rejected...")
        
        # Check if the file exists
        if not os.path.exists(excel_file):
            print(f"Error: The file '{excel_file}' does not exist in the current directory.")
            print(f"Current working directory: {os.getcwd()}")
            print("Please make sure the file is in the correct location.")
            return
        
        # Read the Excel file with skipping 8 rows as before
        df = pd.read_excel(excel_file, skiprows=8)
        
        # Get the awareness column (index 28, which is the 29th column)
        if len(df.columns) <= 28:
            print("Could not find the Fair Fares awareness column (index 28).")
            return
            
        awareness_column = df.columns[28]
        
        # Get the application column (index 29, which is the 30th column)
        if len(df.columns) <= 29:
            print("Could not find the Fair Fares application column (index 29).")
            return
            
        application_column = df.columns[29]
        
        # Get the acceptance column (index 30, which is the 31st column)
        if len(df.columns) <= 30:
            print("Could not find the Fair Fares acceptance column (index 30).")
            return
            
        acceptance_column = df.columns[30]
        
        print(f"Using awareness column at index 28: {awareness_column}")
        print(f"Using application column at index 29: {application_column}")
        print(f"Using acceptance column at index 30: {acceptance_column}")
        
        # Filter for people who applied for Fair Fares (answered 'Yes' to application question)
        applied_people = df[df[application_column] == 'Yes']
        total_applied = len(applied_people)
        
        if total_applied == 0:
            print("No respondents applied for Fair Fares.")
            return
            
        print(f"\nTotal number of people who applied for Fair Fares: {total_applied}")
        
        # Count how many applications were accepted or rejected
        acceptance_counts = applied_people[acceptance_column].value_counts(dropna=False)
        
        # Print individual counts and calculate percentages
        print("\nAcceptance rates among those who applied for Fair Fares:")
        for value, count in acceptance_counts.items():
            value_str = str(value) if not pd.isna(value) else "No response"
            percentage = (count / total_applied) * 100
            print(f"{value_str}: {count} ({percentage:.2f}%)")
            
    except Exception as e:
        print(f"Error in analyze_fair_fares_acceptance: {e}")


def analyze_financial_burden_reduction():
    """
    Analyzes how many people who were accepted into Fair Fares reported reduced financial burden.
    
    This function filters the dataset to include only respondents who were accepted into
    the Fair Fares program, then calculates how many of those respondents reported a
    reduction in their financial burden as a result of the program.
    """
    try:
        print("\n=== ANALYZING FINANCIAL BURDEN REDUCTION FOR ACCEPTED APPLICANTS ===\n")
        print("Analyzing how many people who were accepted into Fair Fares reported reduced financial burden...")
        
        # Check if the file exists
        if not os.path.exists(excel_file):
            print(f"Error: The file '{excel_file}' does not exist in the current directory.")
            print(f"Current working directory: {os.getcwd()}")
            print("Please make sure the file is in the correct location.")
            return
        
        # Read the Excel file with skipping 8 rows as before
        df = pd.read_excel(excel_file, skiprows=8)
        
        # Get the acceptance column (index 30, which is the 31st column)
        if len(df.columns) <= 30:
            print("Could not find the Fair Fares acceptance column (index 30).")
            return
            
        acceptance_column = df.columns[30]
        
        # Get the financial burden column (index 31, which is the 32nd column)
        if len(df.columns) <= 31:
            print("Could not find the financial burden column (index 31).")
            return
            
        financial_burden_column = df.columns[31]
        
        print(f"Using acceptance column at index 30: {acceptance_column}")
        print(f"Using financial burden column at index 31: {financial_burden_column}")
        
        # Filter for people who were accepted into Fair Fares (answered 'Accepted' to acceptance question)
        accepted_people = df[df[acceptance_column] == 'Accepted']
        total_accepted = len(accepted_people)
        
        if total_accepted == 0:
            print("No respondents were accepted into Fair Fares.")
            return
            
        print(f"\nTotal number of people who were accepted into Fair Fares: {total_accepted}")
        
        # Count how many accepted applicants reported reduced financial burden
        financial_burden_counts = accepted_people[financial_burden_column].value_counts(dropna=False)
        
        # Print individual counts and calculate percentages
        print("\nFinancial burden reduction among those accepted into Fair Fares:")
        for value, count in financial_burden_counts.items():
            value_str = str(value) if not pd.isna(value) else "No response"
            percentage = (count / total_accepted) * 100
            print(f"{value_str}: {count} ({percentage:.2f}%)")
            
    except Exception as e:
        print(f"Error in analyze_financial_burden_reduction: {e}")


# -----------------------------------------------------------------------------
# MAIN EXECUTION
# -----------------------------------------------------------------------------

# Call the analysis functions when script is run directly
if __name__ == "__main__":
    analyze_fair_fares_application()
    analyze_fair_fares_acceptance()
    analyze_financial_burden_reduction()