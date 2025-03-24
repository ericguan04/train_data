#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Fair Fares Analysis Script

This script uses the Fair Fares analyzer and visualizer to analyze data from the CUNY MetroCard survey
and generate a Sankey diagram showing the flow of Fair Fares applications through various stages.
"""

import os
import sys
import webbrowser

# Add the parent directory to the path so we can import the data_loader module
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import the required modules
from data_loader import FairFaresDataLoader
from analyzer import FairFaresAnalyzer
from visualization import FairFaresVisualizer


def main():
    """
    Main function to run the Fair Fares analysis and generate visualizations.
    """
    # Define the path to the Excel file
    excel_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'CunyMetroCard191.xlsx')
    
    # Check if the file exists
    if not os.path.exists(excel_file):
        print(f"Error: The file '{excel_file}' does not exist.")
        print(f"Current working directory: {os.getcwd()}")
        print("Please make sure the file is in the correct location.")
        return
    
    # Create a data loader
    print("Creating data loader...")
    data_loader = FairFaresDataLoader(excel_file=excel_file, skiprows=8)
    
    # Create an analyzer
    print("Creating analyzer...")
    analyzer = FairFaresAnalyzer(data_loader)
    
    # Run all analyses
    print("Running analyses...")
    analysis_results = analyzer.run_all_analyses()
    
    # Create a visualizer
    print("Creating visualizer...")
    visualizer = FairFaresVisualizer(analyzer)
    
    # Create a Sankey diagram
    print("Creating Sankey diagram...")
    fig = visualizer.create_sankey_diagram()
    
    # Save the Sankey diagram
    output_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'fair_fares_sankey.html')
    print(f"Saving Sankey diagram to {output_file}...")
    visualizer.save_sankey_diagram(fig, output_file)
    
    print("\nAnalysis complete!")
    print(f"Sankey diagram saved to {output_file}")
    
    # Automatically open the Sankey diagram in the default web browser
    print("Opening Sankey diagram in web browser...")
    webbrowser.open('file://' + os.path.abspath(output_file))


if __name__ == "__main__":
    main()