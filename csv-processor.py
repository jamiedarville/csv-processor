#!/usr/bin/env python3
"""
CSV Processor Script
====================
This script processes a CSV file containing server information and generates
three summary reports:
1. OS Summary - counts of unique operating systems
2. Hostname Summary - counts of unique hostnames  
3. Vulnerability Summary - counts of unique vulnerabilities

Author: Generated Script
Date: 2025
"""

import pandas as pd
import sys
import os
from pathlib import Path
from datetime import datetime # Added import


def process_csv_file(input_file_path, output_directory=None):
    """
    Process the input CSV file and generate three summary reports.
    
    Args:
        input_file_path (str): Path to the input CSV file
        output_directory (str, optional): Directory to save output files. 
                                        Defaults to same directory as input file.
    """
    
    # Validate input file exists
    if not os.path.exists(input_file_path):
        print(f"Error: Input file '{input_file_path}' not found.")
        return False
    
    # Set output directory
    if output_directory is None:
        output_directory = os.path.dirname(input_file_path)
        if not output_directory: # Handle case where input_file_path is just a filename
            output_directory = "." 
    
    # Create output directory if it doesn't exist
    Path(output_directory).mkdir(parents=True, exist_ok=True)

    # Generate a single timestamp for all files from this run
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    try:
        # Read the CSV file
        print(f"Reading CSV file: {input_file_path}")
        df = pd.read_csv(input_file_path)
        
        # Verify the CSV has enough columns
        if len(df.columns) < 8:
            print(f"Warning: CSV file has only {len(df.columns)} columns. Expected at least 8 columns.")
            print("Proceeding with available columns...")
        
        # Extract relevant columns (using 0-based indexing)
        # Column C = index 2, Column E = index 4, Column H = index 7
        hostnames = df.iloc[:, 2] if len(df.columns) > 2 else pd.Series(dtype=str)  # Column C
        operating_systems = df.iloc[:, 4] if len(df.columns) > 4 else pd.Series(dtype=str)  # Column E
        vulnerabilities = df.iloc[:, 7] if len(df.columns) > 7 else pd.Series(dtype=str)  # Column H
        
        # Process Operating Systems Summary
        print("Processing Operating Systems summary...")
        os_summary_path = process_os_summary(operating_systems, output_directory, timestamp)
        
        # Process Hostnames Summary
        print("Processing Hostnames summary...")
        hostname_summary_path = process_hostname_summary(hostnames, output_directory, timestamp)
        
        # Process Vulnerabilities Summary
        print("Processing Vulnerabilities summary...")
        vuln_summary_path = process_vulnerability_summary(vulnerabilities, output_directory, timestamp)
        
        print("\nSummary Reports Generated Successfully!")
        if os_summary_path:
            print(f"- OS Summary: {os_summary_path}")
        if hostname_summary_path:
            print(f"- Hostname Summary: {hostname_summary_path}")
        if vuln_summary_path:
            print(f"- Vulnerability Summary: {vuln_summary_path}")
            
        return True
        
    except Exception as e:
        print(f"Error processing CSV file: {str(e)}")
        return False


def process_os_summary(os_column, output_dir, timestamp):
    """
    Process operating systems data and create summary CSV.
    
    Args:
        os_column (pd.Series): Series containing operating system data
        output_dir (str): Directory to save the output file
        timestamp (str): Timestamp string to append to the filename
    
    Returns:
        str: Path to the saved CSV file or None if error
    """
    
    # Clean the data: strip whitespace and handle null/empty values
    os_cleaned = os_column.astype(str).str.strip()
    
    # Replace empty strings, 'nan', and whitespace-only strings with 'Unknown'
    os_cleaned = os_cleaned.replace(['', 'nan', 'NaN', 'null', 'NULL'], 'Unknown')
    os_cleaned = os_cleaned.replace(r'^\s*$', 'Unknown', regex=True)
    
    # Count occurrences of each OS
    os_counts = os_cleaned.value_counts().reset_index()
    os_counts.columns = ['Operating System', 'Count']
    
    # Sort alphabetically by Operating System
    os_counts = os_counts.sort_values('Operating System').reset_index(drop=True)
    
    # Save to CSV
    filename = f'os_summary_{timestamp}.csv'
    output_path = os.path.join(output_dir, filename)
    try:
        os_counts.to_csv(output_path, index=False)
        print(f"  - Saved OS summary to: {output_path}")
        print(f"  - Found {len(os_counts)} unique operating systems")
        return output_path
    except Exception as e:
        print(f"  - Error saving OS summary: {e}")
        return None


def process_hostname_summary(hostname_column, output_dir, timestamp):
    """
    Process hostnames data and create summary CSV.
    
    Args:
        hostname_column (pd.Series): Series containing hostname data
        output_dir (str): Directory to save the output file
        timestamp (str): Timestamp string to append to the filename

    Returns:
        str: Path to the saved CSV file or None if error
    """
    
    # Clean the data: strip whitespace and remove null/empty values
    hostname_cleaned = hostname_column.astype(str).str.strip()
    
    # Remove empty strings, 'nan', and whitespace-only strings
    hostname_cleaned = hostname_cleaned.replace(['', 'nan', 'NaN', 'null', 'NULL'], pd.NA)
    hostname_cleaned = hostname_cleaned.replace(r'^\s*$', pd.NA, regex=True)
    
    # Drop null values for hostname processing
    hostname_cleaned = hostname_cleaned.dropna()
    
    # Count occurrences of each hostname
    hostname_counts = hostname_cleaned.value_counts().reset_index()
    hostname_counts.columns = ['Hostname', 'Count']
    
    # Sort alphabetically by Hostname
    hostname_counts = hostname_counts.sort_values('Hostname').reset_index(drop=True)
    
    # Save to CSV
    filename = f'hostname_summary_{timestamp}.csv'
    output_path = os.path.join(output_dir, filename)
    try:
        hostname_counts.to_csv(output_path, index=False)
        print(f"  - Saved hostname summary to: {output_path}")
        print(f"  - Found {len(hostname_counts)} unique hostnames")
        return output_path
    except Exception as e:
        print(f"  - Error saving hostname summary: {e}")
        return None

def process_vulnerability_summary(vuln_column, output_dir, timestamp):
    """
    Process vulnerabilities data and create summary CSV.
    
    Args:
        vuln_column (pd.Series): Series containing vulnerability data
        output_dir (str): Directory to save the output file
        timestamp (str): Timestamp string to append to the filename
    
    Returns:
        str: Path to the saved CSV file or None if error
    """
    
    # Clean the data: strip whitespace and remove null/empty values
    vuln_cleaned = vuln_column.astype(str).str.strip()
    
    # Remove empty strings, 'nan', and whitespace-only strings
    vuln_cleaned = vuln_cleaned.replace(['', 'nan', 'NaN', 'null', 'NULL'], pd.NA)
    vuln_cleaned = vuln_cleaned.replace(r'^\s*$', pd.NA, regex=True)
    
    # Drop null values for vulnerability processing
    vuln_cleaned = vuln_cleaned.dropna()
    
    # Count occurrences of each vulnerability
    vuln_counts = vuln_cleaned.value_counts().reset_index()
    vuln_counts.columns = ['Vulnerability', 'Count']
    
    # Sort alphabetically by Vulnerability
    vuln_counts = vuln_counts.sort_values('Vulnerability').reset_index(drop=True)
    
    # Save to CSV
    filename = f'vuln_{timestamp}.csv'
    output_path = os.path.join(output_dir, filename)
    try:
        vuln_counts.to_csv(output_path, index=False)
        print(f"  - Saved vulnerability summary to: {output_path}")
        print(f"  - Found {len(vuln_counts)} unique vulnerabilities")
        return output_path
    except Exception as e:
        print(f"  - Error saving vulnerability summary: {e}")
        return None


def main():
    """
    Main function to handle command line arguments and execute the script.
    """
    
    # Configuration: Set your input file path here
    DEFAULT_INPUT_FILE = "input_data.csv"  # Change this to your CSV file path
    
    # Check if file path is provided as command line argument
    if len(sys.argv) > 1:
        input_file = sys.argv[1]
    else:
        input_file = DEFAULT_INPUT_FILE
        print(f"No input file specified. Using default: {DEFAULT_INPUT_FILE}")
        print("Usage: python csv_processor.py <input_csv_file> [output_directory]")
    
    # Check if output directory is provided as command line argument
    output_dir = None
    if len(sys.argv) > 2:
        output_dir = sys.argv[2]
    
    # Process the CSV file
    success = process_csv_file(input_file, output_dir)
    
    if success:
        print("\n✅ Script completed successfully!")
    else:
        print("\n❌ Script failed to complete.")
        sys.exit(1)


if __name__ == "__main__":
    main()