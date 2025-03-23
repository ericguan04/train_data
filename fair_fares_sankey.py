#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fair Fares Sankey Diagram Generator

This script creates a Sankey diagram to visualize the flow of Fair Fares NYC program
applications, showing awareness, application rates, acceptance rates, and outcomes.
"""

import pandas as pd
import plotly.graph_objects as go
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
# DATA EXTRACTION FUNCTIONS
# -----------------------------------------------------------------------------

def extract_sankey_data():
    """
    Extracts data from the Excel file to create a Sankey diagram showing the flow
    of Fair Fares applications through various stages.
    
    Returns:
        dict: A dictionary containing the data needed for the Sankey diagram.
    """
    try:
        print(f"Reading data from {excel_file}...")
        
        # Read the Excel file with skipping 8 rows as in the original script
        df = pd.read_excel(excel_file, skiprows=8)
        
        # Get the relevant columns
        if len(df.columns) <= 31:
            print("Could not find all required columns.")
            return None
            
        awareness_column = df.columns[28]  # Fair Fares awareness
        application_column = df.columns[29]  # Fair Fares application
        acceptance_column = df.columns[30]  # Application acceptance
        financial_burden_column = df.columns[31]  # Financial burden reduction
        
        print(f"Using awareness column: {awareness_column}")
        print(f"Using application column: {application_column}")
        print(f"Using acceptance column: {acceptance_column}")
        print(f"Using financial burden column: {financial_burden_column}")
        
        # Count total responses
        total_responses = len(df)
        print(f"Total number of survey responses: {total_responses}")
        
        # Count awareness responses
        awareness_counts = df[awareness_column].value_counts(dropna=False)
        aware_count = awareness_counts.get('Yes', 0)
        unaware_count = awareness_counts.get('No', 0)
        no_awareness_response = total_responses - (aware_count + unaware_count)
        
        # Count application responses among those aware
        aware_people = df[df[awareness_column] == 'Yes']
        application_counts = aware_people[application_column].value_counts(dropna=False)
        applied_count = application_counts.get('Yes', 0)
        not_applied_count = application_counts.get('No', 0)
        no_application_response = aware_count - (applied_count + not_applied_count)
        
        # Count acceptance responses among those who applied
        applied_people = df[df[application_column] == 'Yes']
        acceptance_counts = applied_people[acceptance_column].value_counts(dropna=False)
        accepted_count = acceptance_counts.get('Accepted', 0)
        rejected_count = acceptance_counts.get('Rejected', 0)
        pending_count = acceptance_counts.get('Pending', 0)
        no_acceptance_response = applied_count - (accepted_count + rejected_count + pending_count)
        
        # Count financial burden reduction among those accepted
        accepted_people = df[df[acceptance_column] == 'Accepted']
        financial_burden_counts = accepted_people[financial_burden_column].value_counts(dropna=False)
        reduced_burden_count = financial_burden_counts.get('Yes', 0)
        not_reduced_burden_count = financial_burden_counts.get('No', 0)
        no_burden_response = accepted_count - (reduced_burden_count + not_reduced_burden_count)
        
        # Create a dictionary with the data for the Sankey diagram
        sankey_data = {
            'total_responses': total_responses,
            'aware_count': aware_count,
            'unaware_count': unaware_count,
            'no_awareness_response': no_awareness_response,
            'applied_count': applied_count,
            'not_applied_count': not_applied_count,
            'no_application_response': no_application_response,
            'accepted_count': accepted_count,
            'rejected_count': rejected_count,
            'pending_count': pending_count,
            'no_acceptance_response': no_acceptance_response,
            'reduced_burden_count': reduced_burden_count,
            'not_reduced_burden_count': not_reduced_burden_count,
            'no_burden_response': no_burden_response
        }
        
        return sankey_data
        
    except Exception as e:
        print(f"Error in extract_sankey_data: {e}")
        return None

# -----------------------------------------------------------------------------
# VISUALIZATION FUNCTIONS
# -----------------------------------------------------------------------------

def create_sankey_diagram(sankey_data):
    """
    Creates a Sankey diagram to visualize the flow of Fair Fares applications.
    
    Args:
        sankey_data (dict): A dictionary containing the data needed for the Sankey diagram.
        
    Returns:
        plotly.graph_objects.Figure: A Plotly figure object containing the Sankey diagram.
    """
    if sankey_data is None:
        print("No data available to create Sankey diagram.")
        return None
    
    # Define the nodes (stages in the application process)
    nodes = [
        {'label': 'Total Responses'},  # 0
        {'label': 'Aware of Fair Fares'},  # 1
        {'label': 'Unaware of Fair Fares'},  # 2
        {'label': 'No Awareness Response'},  # 3
        {'label': 'Applied'},  # 4
        {'label': 'Did Not Apply'},  # 5
        {'label': 'No Application Response'},  # 6
        {'label': 'Accepted'},  # 7
        {'label': 'Rejected'},  # 8
        {'label': 'Pending'},  # 9
        {'label': 'No Acceptance Response'},  # 10
        {'label': 'Reduced Financial Burden'},  # 11
        {'label': 'No Reduction in Financial Burden'},  # 12
        {'label': 'No Financial Burden Response'}  # 13
    ]
    
    # Define the links (flows between stages)
    links = [
        # From Total Responses to Awareness categories
        {'source': 0, 'target': 1, 'value': sankey_data['aware_count'], 'label': f"{sankey_data['aware_count']} Aware"},
        {'source': 0, 'target': 2, 'value': sankey_data['unaware_count'], 'label': f"{sankey_data['unaware_count']} Unaware"},
        {'source': 0, 'target': 3, 'value': sankey_data['no_awareness_response'], 'label': f"{sankey_data['no_awareness_response']} No Response"},
        
        # From Aware to Application categories
        {'source': 1, 'target': 4, 'value': sankey_data['applied_count'], 'label': f"{sankey_data['applied_count']} Applied"},
        {'source': 1, 'target': 5, 'value': sankey_data['not_applied_count'], 'label': f"{sankey_data['not_applied_count']} Did Not Apply"},
        {'source': 1, 'target': 6, 'value': sankey_data['no_application_response'], 'label': f"{sankey_data['no_application_response']} No Response"},
        
        # From Applied to Acceptance categories
        {'source': 4, 'target': 7, 'value': sankey_data['accepted_count'], 'label': f"{sankey_data['accepted_count']} Accepted"},
        {'source': 4, 'target': 8, 'value': sankey_data['rejected_count'], 'label': f"{sankey_data['rejected_count']} Rejected"},
        {'source': 4, 'target': 9, 'value': sankey_data['pending_count'], 'label': f"{sankey_data['pending_count']} Pending"},
        {'source': 4, 'target': 10, 'value': sankey_data['no_acceptance_response'], 'label': f"{sankey_data['no_acceptance_response']} No Response"},
        
        # From Accepted to Financial Burden categories
        {'source': 7, 'target': 11, 'value': sankey_data['reduced_burden_count'], 'label': f"{sankey_data['reduced_burden_count']} Reduced"},
        {'source': 7, 'target': 12, 'value': sankey_data['not_reduced_burden_count'], 'label': f"{sankey_data['not_reduced_burden_count']} Not Reduced"},
        {'source': 7, 'target': 13, 'value': sankey_data['no_burden_response'], 'label': f"{sankey_data['no_burden_response']} No Response"}
    ]
    
    # Create the Sankey diagram
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=[node['label'] for node in nodes],
            color=["rgba(31, 119, 180, 0.8)",  # Total Responses
                   "rgba(255, 127, 14, 0.8)",  # Aware
                   "rgba(44, 160, 44, 0.8)",  # Unaware
                   "rgba(214, 39, 40, 0.8)",  # No Awareness Response
                   "rgba(148, 103, 189, 0.8)",  # Applied
                   "rgba(140, 86, 75, 0.8)",  # Did Not Apply
                   "rgba(227, 119, 194, 0.8)",  # No Application Response
                   "rgba(127, 127, 127, 0.8)",  # Accepted
                   "rgba(188, 189, 34, 0.8)",  # Rejected
                   "rgba(23, 190, 207, 0.8)",  # Pending
                   "rgba(31, 119, 180, 0.8)",  # No Acceptance Response
                   "rgba(255, 127, 14, 0.8)",  # Reduced Financial Burden
                   "rgba(44, 160, 44, 0.8)",  # No Reduction in Financial Burden
                   "rgba(214, 39, 40, 0.8)"]  # No Financial Burden Response
        ),
        link=dict(
            source=[link['source'] for link in links],
            target=[link['target'] for link in links],
            value=[link['value'] for link in links],
            label=[link['label'] for link in links],
            color=["rgba(31, 119, 180, 0.4)",  # Total to Aware
                   "rgba(255, 127, 14, 0.4)",  # Total to Unaware
                   "rgba(44, 160, 44, 0.4)",  # Total to No Awareness Response
                   "rgba(214, 39, 40, 0.4)",  # Aware to Applied
                   "rgba(148, 103, 189, 0.4)",  # Aware to Did Not Apply
                   "rgba(140, 86, 75, 0.4)",  # Aware to No Application Response
                   "rgba(227, 119, 194, 0.4)",  # Applied to Accepted
                   "rgba(127, 127, 127, 0.4)",  # Applied to Rejected
                   "rgba(188, 189, 34, 0.4)",  # Applied to Pending
                   "rgba(23, 190, 207, 0.4)",  # Applied to No Acceptance Response
                   "rgba(31, 119, 180, 0.4)",  # Accepted to Reduced
                   "rgba(255, 127, 14, 0.4)",  # Accepted to Not Reduced
                   "rgba(44, 160, 44, 0.4)"]  # Accepted to No Burden Response
        )
    )])
    
    # Update the layout
    fig.update_layout(
        title_text="Fair Fares NYC Program Application Flow",
        font_size=12,
        width=1000,
        height=800
    )
    
    return fig

# -----------------------------------------------------------------------------
# MAIN EXECUTION
# -----------------------------------------------------------------------------

def main():
    """
    Main function to extract data and create the Sankey diagram.
    """
    # Extract the data for the Sankey diagram
    sankey_data = extract_sankey_data()
    
    if sankey_data is not None:
        # Create the Sankey diagram
        fig = create_sankey_diagram(sankey_data)
        
        if fig is not None:
            # Save the figure as an HTML file
            output_file = 'fair_fares_sankey.html'
            fig.write_html(output_file)
            print(f"Sankey diagram saved to {output_file}")
            
            # Show the figure
            fig.show()
    
    print("Done.")

# Call the main function when script is run directly
if __name__ == "__main__":
    main()