#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Analyzer Module for Fair Fares Analysis

This module provides functions for analyzing Fair Fares NYC program data,
including awareness, application rates, acceptance rates, and financial impact.
"""

import pandas as pd


class FairFaresAnalyzer:
    """
    A class to analyze Fair Fares data from the CUNY MetroCard survey.
    """
    
    def __init__(self, data_loader):
        """
        Initialize the analyzer with a data loader.
        
        Args:
            data_loader (FairFaresDataLoader): A data loader object with loaded data.
        """
        self.data_loader = data_loader
        self.df = data_loader.df
    
    def analyze_awareness(self):
        """
        Analyze awareness of the Fair Fares program among survey respondents.
        
        Returns:
            dict: A dictionary containing awareness statistics.
        """
        if self.df is None:
            print("No data loaded. Please load data first.")
            return None
        
        awareness_column = self.data_loader.get_awareness_column()
        if awareness_column is None:
            return None
        
        print(f"\n=== ANALYZING FAIR FARES AWARENESS ===\n")
        print(f"Using awareness column: {awareness_column}")
        
        # Count responses
        value_counts = self.df[awareness_column].value_counts(dropna=False)
        total_responses = sum(value_counts)
        
        print(f"Total number of responses: {total_responses}")
        
        # Print individual counts and calculate percentages
        print("\nResponse counts and percentages:")
        results = {}
        for value, count in value_counts.items():
            value_str = str(value) if not pd.isna(value) else "No response"
            percentage = (count / total_responses) * 100
            print(f"{value_str}: {count} ({percentage:.2f}%)")
            results[value_str] = {'count': count, 'percentage': percentage}
        
        return {
            'total_responses': total_responses,
            'results': results
        }
    
    def analyze_application_rates(self):
        """
        Analyze how many people who were aware of Fair Fares actually applied for it.
        
        Returns:
            dict: A dictionary containing application rate statistics.
        """
        if self.df is None:
            print("No data loaded. Please load data first.")
            return None
        
        print("\n=== ANALYZING FAIR FARES APPLICATION RATES ===\n")
        print("Analyzing how many people who were aware of Fair Fares actually applied for it...")
        
        awareness_column = self.data_loader.get_awareness_column()
        application_column = self.data_loader.get_application_column()
        
        if awareness_column is None or application_column is None:
            return None
        
        print(f"Using awareness column: {awareness_column}")
        print(f"Using application column: {application_column}")
        
        # Filter for people who were aware of Fair Fares (answered 'Yes')
        aware_people = self.df[self.df[awareness_column] == 'Yes']
        total_aware = len(aware_people)
        
        if total_aware == 0:
            print("No respondents were aware of Fair Fares.")
            return None
        
        print(f"\nTotal number of people aware of Fair Fares: {total_aware}")
        
        # Count how many of those aware people applied for Fair Fares
        application_counts = aware_people[application_column].value_counts(dropna=False)
        
        # Print individual counts and calculate percentages
        print("\nApplication rates among those aware of Fair Fares:")
        results = {}
        for value, count in application_counts.items():
            value_str = str(value) if not pd.isna(value) else "No response"
            percentage = (count / total_aware) * 100
            print(f"{value_str}: {count} ({percentage:.2f}%)")
            results[value_str] = {'count': count, 'percentage': percentage}
        
        return {
            'total_aware': total_aware,
            'results': results
        }
    
    def analyze_acceptance_rates(self):
        """
        Analyze how many Fair Fares applications were accepted or rejected.
        
        Returns:
            dict: A dictionary containing acceptance rate statistics.
        """
        if self.df is None:
            print("No data loaded. Please load data first.")
            return None
        
        print("\n=== ANALYZING FAIR FARES ACCEPTANCE RATES ===\n")
        print("Analyzing how many Fair Fares applications were accepted or rejected...")
        
        awareness_column = self.data_loader.get_awareness_column()
        application_column = self.data_loader.get_application_column()
        acceptance_column = self.data_loader.get_acceptance_column()
        
        if awareness_column is None or application_column is None or acceptance_column is None:
            return None
        
        print(f"Using awareness column: {awareness_column}")
        print(f"Using application column: {application_column}")
        print(f"Using acceptance column: {acceptance_column}")
        
        # Filter for people who applied for Fair Fares (answered 'Yes' to application question)
        applied_people = self.df[self.df[application_column] == 'Yes']
        total_applied = len(applied_people)
        
        if total_applied == 0:
            print("No respondents applied for Fair Fares.")
            return None
        
        print(f"\nTotal number of people who applied for Fair Fares: {total_applied}")
        
        # Count how many applications were accepted or rejected
        acceptance_counts = applied_people[acceptance_column].value_counts(dropna=False)
        
        # Print individual counts and calculate percentages
        print("\nAcceptance rates among Fair Fares applicants:")
        results = {}
        for value, count in acceptance_counts.items():
            value_str = str(value) if not pd.isna(value) else "No response"
            percentage = (count / total_applied) * 100
            print(f"{value_str}: {count} ({percentage:.2f}%)")
            results[value_str] = {'count': count, 'percentage': percentage}
        
        return {
            'total_applied': total_applied,
            'results': results
        }
    
    def analyze_financial_burden_reduction(self):
        """
        Analyze how many people who were accepted into Fair Fares reported reduced financial burden.
        
        Returns:
            dict: A dictionary containing financial burden reduction statistics.
        """
        if self.df is None:
            print("No data loaded. Please load data first.")
            return None
        
        print("\n=== ANALYZING FINANCIAL BURDEN REDUCTION FOR ACCEPTED APPLICANTS ===\n")
        print("Analyzing how many people who were accepted into Fair Fares reported reduced financial burden...")
        
        acceptance_column = self.data_loader.get_acceptance_column()
        financial_burden_column = self.data_loader.get_financial_burden_column()
        
        if acceptance_column is None or financial_burden_column is None:
            return None
        
        print(f"Using acceptance column: {acceptance_column}")
        print(f"Using financial burden column: {financial_burden_column}")
        
        # Filter for people who were accepted into Fair Fares (answered 'Accepted' to acceptance question)
        accepted_people = self.df[self.df[acceptance_column] == 'Accepted']
        total_accepted = len(accepted_people)
        
        if total_accepted == 0:
            print("No respondents were accepted into Fair Fares.")
            return None
        
        print(f"\nTotal number of people who were accepted into Fair Fares: {total_accepted}")
        
        # Count how many accepted applicants reported reduced financial burden
        financial_burden_counts = accepted_people[financial_burden_column].value_counts(dropna=False)
        
        # Print individual counts and calculate percentages
        print("\nFinancial burden reduction among those accepted into Fair Fares:")
        results = {}
        for value, count in financial_burden_counts.items():
            value_str = str(value) if not pd.isna(value) else "No response"
            percentage = (count / total_accepted) * 100
            print(f"{value_str}: {count} ({percentage:.2f}%)")
            results[value_str] = {'count': count, 'percentage': percentage}
        
        return {
            'total_accepted': total_accepted,
            'results': results
        }
    
    def run_all_analyses(self):
        """
        Run all analysis functions and return a dictionary with all results.
        
        Returns:
            dict: A dictionary containing all analysis results.
        """
        results = {}
        
        # Run all analyses
        print("\n=== RUNNING ALL FAIR FARES ANALYSES ===\n")
        
        # Analyze awareness
        awareness_results = self.analyze_awareness()
        if awareness_results:
            results['awareness'] = awareness_results
        
        # Analyze application rates
        application_results = self.analyze_application_rates()
        if application_results:
            results['application'] = application_results
        
        # Analyze acceptance rates
        acceptance_results = self.analyze_acceptance_rates()
        if acceptance_results:
            results['acceptance'] = acceptance_results
        
        # Analyze financial burden reduction
        financial_burden_results = self.analyze_financial_burden_reduction()
        if financial_burden_results:
            results['financial_burden'] = financial_burden_results
        
        return results