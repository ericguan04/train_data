#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Data Loader Module for Fair Fares Analysis

This module provides functions for loading and preprocessing Fair Fares NYC program data
from the CUNY MetroCard survey.
"""

import pandas as pd
import os


class FairFaresDataLoader:
    """
    A class to load and preprocess Fair Fares data from the CUNY MetroCard survey.
    """
    
    def __init__(self, excel_file='CunyMetroCard191.xlsx', skiprows=8):
        """
        Initialize the data loader with the path to the Excel file.
        
        Args:
            excel_file (str): The path to the Excel file containing the survey data.
            skiprows (int): The number of rows to skip when reading the Excel file.
        """
        self.excel_file = excel_file
        self.skiprows = skiprows
        self.df = None
        self.column_indices = {
            'awareness': 28,  # Fair Fares awareness column index
            'application': 29,  # Fair Fares application column index
            'acceptance': 30,  # Application acceptance column index
            'financial_burden': 31  # Financial burden reduction column index
        }
        
        # Load the data
        self.load_data()
    
    def load_data(self):
        """
        Load the data from the Excel file.
        
        Returns:
            bool: True if the data was loaded successfully, False otherwise.
        """
        try:
            # Check if the file exists
            if not os.path.exists(self.excel_file):
                print(f"Error: The file '{self.excel_file}' does not exist in the current directory.")
                print(f"Current working directory: {os.getcwd()}")
                print("Please make sure the file is in the correct location.")
                return False
            
            # Read the Excel file
            print(f"Reading data from {self.excel_file}...")
            self.df = pd.read_excel(self.excel_file, skiprows=self.skiprows)
            
            print(f"Data loaded successfully. Shape: {self.df.shape}")
            return True
            
        except Exception as e:
            print(f"Error loading data: {e}")
            return False
    
    def get_awareness_column(self):
        """
        Get the name of the column containing Fair Fares awareness data.
        
        Returns:
            str: The name of the awareness column, or None if it doesn't exist.
        """
        if self.df is None or len(self.df.columns) <= self.column_indices['awareness']:
            print("Could not find the Fair Fares awareness column.")
            return None
        
        awareness_column = self.df.columns[self.column_indices['awareness']]
        return awareness_column
    
    def get_application_column(self):
        """
        Get the name of the column containing Fair Fares application data.
        
        Returns:
            str: The name of the application column, or None if it doesn't exist.
        """
        if self.df is None or len(self.df.columns) <= self.column_indices['application']:
            print("Could not find the Fair Fares application column.")
            return None
        
        application_column = self.df.columns[self.column_indices['application']]
        return application_column
    
    def get_acceptance_column(self):
        """
        Get the name of the column containing Fair Fares acceptance data.
        
        Returns:
            str: The name of the acceptance column, or None if it doesn't exist.
        """
        if self.df is None or len(self.df.columns) <= self.column_indices['acceptance']:
            print("Could not find the Fair Fares acceptance column.")
            return None
        
        acceptance_column = self.df.columns[self.column_indices['acceptance']]
        return acceptance_column
    
    def get_financial_burden_column(self):
        """
        Get the name of the column containing financial burden reduction data.
        
        Returns:
            str: The name of the financial burden column, or None if it doesn't exist.
        """
        if self.df is None or len(self.df.columns) <= self.column_indices['financial_burden']:
            print("Could not find the Fair Fares financial burden column.")
            return None
        
        financial_burden_column = self.df.columns[self.column_indices['financial_burden']]
        return financial_burden_column