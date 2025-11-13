"""
main.py

This script serves as the main entry point for the Towers of Hanoi Performance
Analyzer program.

Its sole responsibility is to define and manage the command-line interface (CLI)
that the user interacts with. It uses the `argparse` module to handle user
input, including the required input file and optional flags for customizing
the output.

Once the arguments are parsed, it passes them to the `process_and_write_results`
function in the `reporting` module, which handles all the core logic.

Author: Alfredo Ormeno Zuniga
Date: 10/6/2025
"""

import argparse
from reporting import process_and_write_results

def main():
    """
    Sets up the command-line argument parser, parses the user-provided
    arguments, and then calls the main processing function.
    """
     
    parser = argparse.ArgumentParser(description="Solve Towers of Hanoi and write results to a file.")
    parser.add_argument("input_file", help="Required: Path to the input file.")
    parser.add_argument("-o", "--output", default="output.txt", help="Optional: Path to the output file (default: output.txt).")
    parser.add_argument("-d", "--display", action="store_true", help="Optional: Flag to include the move list in the output file.")
    parser.add_argument("-g", "--graph", action="store_true", help="Optional: Flag to generate and append bar graph of the results.")
    
    args = parser.parse_args()

    process_and_write_results(args.input_file, args.output, args.display, args.graph)


if __name__ == "__main__":
    main()