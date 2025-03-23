import pandas as pd
import os
import matplotlib.pyplot as plt
from datetime import datetime

# Define the path to the Excel file
excel_file = 'CunyMetroCard191.xlsx'

# Check if the file exists
if not os.path.exists(excel_file):
    print(f"Error: The file '{excel_file}' does not exist in the current directory.")
    print(f"Current working directory: {os.getcwd()}")
    print("Please make sure the file is in the correct location.")
    exit(1)

try:
    # Read the Excel file
    print(f"Reading data from {excel_file}...")
    df = pd.read_excel(excel_file)
    
    # Create a directory for reports if it doesn't exist
    if not os.path.exists('reports'):
        os.makedirs('reports')
    
    # Create a report file
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = f"reports/fair_fares_report_{timestamp}.txt"
    
    with open(report_file, 'w') as f:
        # Write basic information about the dataset
        f.write("=== FAIR FARES AWARENESS REPORT ===\n\n")
        f.write(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Dataset: {excel_file}\n")
        f.write(f"Number of respondents: {df.shape[0]}\n")
        f.write(f"Number of questions: {df.shape[1]}\n\n")
        
        # Write all columns in the dataset
        f.write("=== COLUMNS IN THE DATASET ===\n\n")
        for i, column in enumerate(df.columns, 1):
            f.write(f"{i}. {column}\n")
        
        # Analyze Fair Fares awareness
        f.write("\n=== FAIR FARES AWARENESS ANALYSIS ===\n\n")
        
        # Look for Fair Fares awareness column
        fair_fares_columns = [col for col in df.columns if 'fair fare' in col.lower()]
        
        if fair_fares_columns:
            for col in fair_fares_columns:
                f.write(f"Column: {col}\n\n")
                
                # Count responses
                value_counts = df[col].value_counts(dropna=False)
                f.write("Response counts:\n")
                for value, count in value_counts.items():
                    value_str = str(value) if not pd.isna(value) else "No response"
                    f.write(f"{value_str}: {count}\n")
                
                # Calculate percentages
                percentages = df[col].value_counts(normalize=True, dropna=False) * 100
                f.write("\nResponse percentages:\n")
                for value, percentage in percentages.items():
                    value_str = str(value) if not pd.isna(value) else "No response"
                    f.write(f"{value_str}: {percentage:.2f}%\n")
                
                # Create a pie chart for visualization
                plt.figure(figsize=(8, 6))
                plt.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%', startangle=90)
                plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle
                plt.title(f'Fair Fares Awareness: {col}')
                chart_file = f"reports/fair_fares_awareness_{col.replace(' ', '_')}_{timestamp}.png"
                plt.savefig(chart_file)
                f.write(f"\nPie chart saved as '{chart_file}'\n\n")
                
                # If this is the awareness column, print a summary
                if 'aware' in col.lower():
                    aware_count = df[df[col] == 'Yes'].shape[0]
                    not_aware_count = df[df[col] == 'No'].shape[0]
                    total_responses = aware_count + not_aware_count
                    
                    f.write("\n=== SUMMARY OF FAIR FARES AWARENESS ===\n\n")
                    f.write(f"Total respondents: {total_responses}\n")
                    f.write(f"Aware of Fair Fares: {aware_count} ({aware_count/total_responses*100:.2f}%)\n")
                    f.write(f"Not aware of Fair Fares: {not_aware_count} ({not_aware_count/total_responses*100:.2f}%)\n")
        else:
            f.write("No column containing 'Fair Fare' was found in the dataset.\n")
    
    print(f"\nReport generated successfully: {report_file}")
    
    # Print a summary to the console
    awareness_col = next((col for col in df.columns if 'aware' in col.lower() and 'fair fare' in col.lower()), None)
    if awareness_col:
        aware_count = df[df[awareness_col] == 'Yes'].shape[0]
        not_aware_count = df[df[awareness_col] == 'No'].shape[0]
        total_responses = aware_count + not_aware_count
        
        print("\n=== SUMMARY OF FAIR FARES AWARENESS ===\n")
        print(f"Total respondents: {total_responses}")
        print(f"Aware of Fair Fares: {aware_count} ({aware_count/total_responses*100:.2f}%)")
        print(f"Not aware of Fair Fares: {not_aware_count} ({not_aware_count/total_responses*100:.2f}%)")

except Exception as e:
    print(f"Error: {e}")