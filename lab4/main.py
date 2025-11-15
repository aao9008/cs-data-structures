"""
main.py
Author: Alfredo Ormeno Zuniga
Date: 11/15/2025

Main entry point for the sorting lab. This program 
serves as a command-line interface to run a series of
sorting experiments. It accepts a mandatory input folder
and optional output paths, then calls the 'lab_runner'
module to perform all data processing, sorting, and timing.
"""

import lab_runner
import os
import argparse  # Import the argparse library

def main():
    """
    Main entry point for the sorting lab project.

    Parses command-line arguments and calls the main experiment
    runner function from the 'lab_runner' module.
    """
    
    # --- 1. Setup Argument Parser ---
    parser = argparse.ArgumentParser(
        description="Run sorting algorithm performance experiments."
    )
    
    # --- 2. Define Arguments ---
    
    # Mandatory Positional Argument
    parser.add_argument(
        "input_folder",  # This is the name of the argument
        type=str,
        help="Path to the folder containing the input data files (.dat, .txt)."
    )
    
    # Optional Argument for Output Directory
    parser.add_argument(
        "-o", "--output_dir",
        type=str,
        default="sorted_results",
        help="Directory to store sorted output files (default: 'sorted_results')."
    )
    
    # Optional Argument for Timings File
    parser.add_argument(
        "-t", "--timings_file",
        type=str,
        default="timings_table.csv",
        help="File path for the CSV timings table (default: 'timings_table.csv')."
    )
    
    # --- 3. Parse Arguments ---
    args = parser.parse_args()

    # --- 4. Run Experiments ---
    
    # Check if the input folder exists before running
    if not os.path.exists(args.input_folder):
        print(f"Error: Input folder not found at '{args.input_folder}'.")
        print("Please provide a valid path to the input data folder.")
    else:
        # Call the main runner function with the configured paths
        # from the command line
        lab_runner.run_sorting_experiments(
            input_folder=args.input_folder,
            output_dir=args.output_dir,
            timings_filepath=args.timings_file
        )

if __name__ == "__main__":
    main()