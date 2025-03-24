#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Visualization Module for Fair Fares Analysis

This module provides functions for creating visualizations of Fair Fares NYC program data,
including Sankey diagrams to show the flow of applications through the program.
"""

import plotly.graph_objects as go


class FairFaresVisualizer:
    """
    A class to create visualizations of Fair Fares data.
    """
    
    def __init__(self, analyzer):
        """
        Initialize the visualizer with an analyzer.
        
        Args:
            analyzer (FairFaresAnalyzer): An analyzer object with analysis results.
        """
        self.analyzer = analyzer
    
    def extract_sankey_data(self):
        """
        Extract data from the analyzer to create a Sankey diagram showing the flow
        of Fair Fares applications through various stages.
        
        Returns:
            dict: A dictionary containing the data needed for the Sankey diagram.
        """
        try:
            # Run all analyses to get the data
            analysis_results = self.analyzer.run_all_analyses()
            if not analysis_results:
                print("No analysis results available.")
                return None
            
            # Extract data from analysis results
            awareness_results = analysis_results.get('awareness', {})
            application_results = analysis_results.get('application', {})
            acceptance_results = analysis_results.get('acceptance', {})
            financial_burden_results = analysis_results.get('financial_burden', {})
            
            # Get total responses
            total_responses = awareness_results.get('total_responses', 0)
            
            # Get awareness counts
            awareness_data = awareness_results.get('results', {})
            aware_count = awareness_data.get('Yes', {}).get('count', 0)
            unaware_count = awareness_data.get('No', {}).get('count', 0)
            no_awareness_response = total_responses - (aware_count + unaware_count)
            
            # Get application counts
            application_data = application_results.get('results', {})
            applied_count = application_data.get('Yes', {}).get('count', 0)
            not_applied_count = application_data.get('No', {}).get('count', 0)
            no_application_response = awareness_data.get('Yes', {}).get('count', 0) - (applied_count + not_applied_count)
            
            # Get acceptance counts
            acceptance_data = acceptance_results.get('results', {})
            accepted_count = acceptance_data.get('Accepted', {}).get('count', 0)
            rejected_count = acceptance_data.get('Rejected', {}).get('count', 0)
            pending_count = acceptance_data.get('Pending', {}).get('count', 0)
            no_acceptance_response = application_data.get('Yes', {}).get('count', 0) - (accepted_count + rejected_count + pending_count)
            
            # Get financial burden reduction counts
            financial_burden_data = financial_burden_results.get('results', {})
            reduced_burden_count = financial_burden_data.get('Yes', {}).get('count', 0)
            not_reduced_burden_count = financial_burden_data.get('No', {}).get('count', 0)
            no_burden_response = acceptance_data.get('Accepted', {}).get('count', 0) - (reduced_burden_count + not_reduced_burden_count)
            
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
    
    def create_sankey_diagram(self, sankey_data=None):
        """
        Creates a Sankey diagram to visualize the flow of Fair Fares applications.
        
        Args:
            sankey_data (dict, optional): A dictionary containing the data needed for the Sankey diagram.
                If None, the data will be extracted from the analyzer.
                
        Returns:
            plotly.graph_objects.Figure: A Plotly figure object containing the Sankey diagram.
        """
        if sankey_data is None:
            sankey_data = self.extract_sankey_data()
        
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
        
        # Create the Sankey diagram with enhanced UI
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=20,  # Increased padding for better spacing
                thickness=25,  # Increased thickness for better visibility
                line=dict(color="rgba(50, 50, 50, 0.5)", width=0.8),  # Improved border
                label=[node['label'] for node in nodes],
                # Enhanced color palette with better contrast
                color=["rgba(31, 119, 180, 0.9)",  # Total Responses - deeper blue
                       "rgba(255, 127, 14, 0.9)",  # Aware - vibrant orange
                       "rgba(44, 160, 44, 0.9)",  # Unaware - rich green
                       "rgba(214, 39, 40, 0.9)",  # No Awareness Response - bright red
                       "rgba(148, 103, 189, 0.9)",  # Applied - deep purple
                       "rgba(140, 86, 75, 0.9)",  # Did Not Apply - brown
                       "rgba(227, 119, 194, 0.9)",  # No Application Response - pink
                       "rgba(127, 127, 127, 0.9)",  # Accepted - gray
                       "rgba(188, 189, 34, 0.9)",  # Rejected - yellow-green
                       "rgba(23, 190, 207, 0.9)",  # Pending - cyan
                       "rgba(31, 119, 180, 0.9)",  # No Acceptance Response - blue
                       "rgba(255, 127, 14, 0.9)",  # Reduced Financial Burden - orange
                       "rgba(44, 160, 44, 0.9)",  # No Reduction in Financial Burden - green
                       "rgba(214, 39, 40, 0.9)"],  # No Financial Burden Response - red
            ),
            link=dict(
                source=[link['source'] for link in links],
                target=[link['target'] for link in links],
                value=[link['value'] for link in links],
                label=[link['label'] for link in links],
                # Improved link colors with better transparency
                color=["rgba(31, 119, 180, 0.4)",  # Aware - blue
                       "rgba(44, 160, 44, 0.4)",  # Unaware - green
                       "rgba(214, 39, 40, 0.4)",  # No Awareness Response - red
                       "rgba(148, 103, 189, 0.4)",  # Applied - purple
                       "rgba(140, 86, 75, 0.4)",  # Did Not Apply - brown
                       "rgba(227, 119, 194, 0.4)",  # No Application Response - pink
                       "rgba(127, 127, 127, 0.4)",  # Accepted - gray
                       "rgba(188, 189, 34, 0.4)",  # Rejected - yellow-green
                       "rgba(23, 190, 207, 0.4)",  # Pending - cyan
                       "rgba(31, 119, 180, 0.4)",  # No Acceptance Response - blue
                       "rgba(255, 127, 14, 0.4)",  # Reduced Financial Burden - orange
                       "rgba(44, 160, 44, 0.4)",  # Not Reduced Financial Burden - green
                       "rgba(214, 39, 40, 0.4)"]  # No Financial Burden Response - red
            )
        )])
        
        # Update the layout for better presentation
        fig.update_layout(
            title_text="Fair Fares NYC Program Flow",
            font=dict(size=14, family="Arial"),
            paper_bgcolor='rgba(255, 255, 255, 0.9)',
            plot_bgcolor='rgba(255, 255, 255, 0.9)',
            height=800,  # Increased height for better visibility
            width=1200,  # Increased width for better spacing
            margin=dict(l=25, r=25, t=50, b=25),  # Adjusted margins
            title_font=dict(size=24, family="Arial", color="rgba(0, 0, 0, 0.8)"),  # Enhanced title
        )
        
        return fig
    
    def save_sankey_diagram(self, fig, output_file='fair_fares_sankey.html'):
        """
        Saves the Sankey diagram to an HTML file.
        
        Args:
            fig (plotly.graph_objects.Figure): A Plotly figure object containing the Sankey diagram.
            output_file (str, optional): The name of the output file. Defaults to 'fair_fares_sankey.html'.
        """
        if fig is None:
            print("No figure to save.")
            return
        
        try:
            fig.write_html(output_file)
            print(f"Sankey diagram saved to {output_file}")
        except Exception as e:
            print(f"Error saving Sankey diagram: {e}")