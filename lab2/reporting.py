"""
reporting.py

This module contains all the logic for processing, reporting, and visualizing
the performance results of the Towers of Hanoi solvers.

Its primary responsibilities include:
- Reading puzzle configurations from an input file.
- Orchestrating the timing of both the recursive and iterative solvers.
- Writing detailed, formatted reports for each puzzle to a text file.
- Generating a final summary table of all performance metrics.
- Creating and saving a graphical bar chart of the results using matplotlib.

Author: Alfredo Ormeno Zuniga
Date: 10/6/2025
"""

import time
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
from towers_of_hanoi import TowersOfHanoi

def write_summary_table(file_handle, results_data):
    """Writes a formatted summary table of all timing results to a file.

    This function takes a list of result dictionaries and writes a fixed-width,
    human-readable summary table to the provided open file object.

    Args:
        file_handle (TextIOWrapper): An open file object to which the summary
            table will be written. It should be opened in write or append mode.
        results_data (list[dict]): A list of dictionaries, where each
            dictionary contains the performance results for a single puzzle.
            Expected keys: 'disks', 'recursive_time', 'iterative_time'.

    Returns:
        None
    """
    file_handle.write("\n\n--- Performance Summary ---\n")
    # Write table header
    file_handle.write(f"{'Disks':<10} | {'Recursive Time (s)':<22} | {'Iterative Time (s)':<22}\n")
    file_handle.write(f"{'-'*10} | {'-'*22} | {'-'*22}\n")
    
    # Write a row for each result collected
    for result in results_data:
        disks = result['disks']
        rec_time = f"{result['recursive_time']:.6f}"
        iter_time = f"{result['iterative_time']:.6f}"
        file_handle.write(f"{disks:<10} | {rec_time:<22} | {iter_time:<22}\n")

def save_graph_image(results_data, graph_filename):
    """Generates and saves a bar graph visualizing the performance results.

    This function creates a grouped bar chart comparing the run times of the
    recursive and iterative solutions. To handle the wide range of data values,
    it uses a logarithmic scale for the y-axis and dynamically formats the labels
    to display times in seconds (s), milliseconds (ms), or microseconds (µs)
    for enhanced readability.

    Args:
        results_data (list[dict]): A list of dictionaries containing the timing
            results. Each dictionary should have the keys 'disks',
            'recursive_time', and 'iterative_time'.
        graph_filename (str): The path and filename where the generated .png
            image of the graph will be saved.

    Side Effects:
        Creates and saves a .png file to the specified path.

    Returns:
        None
    """
    print(f"Generating and saving graph to '{graph_filename}'...")

    # Define a nested helper function to dynamically format time values for labels.
    # This makes the y-axis and bar labels easy to read at any scale.
    def time_formatter(x, pos):
        """Converts a time in seconds to a formatted string in s, ms, or µs."""
        if x >= 1:
            return f'{x:.2f} s'       # Seconds for large values
        elif x >= 1e-3:
            return f'{x * 1e3:.2f} ms' # Milliseconds for medium values
        else:
            return f'{x * 1e6:.2f} µs' # Microseconds for small values

    # --- 1. Prepare Data for Plotting ---
    labels = [result['disks'] for result in results_data]
    rec_times = [result['recursive_time'] for result in results_data]
    iter_times = [result['iterative_time'] for result in results_data]

    # A logarithmic scale cannot plot zero or negative numbers.
    # We replace any potential zero-second results with a tiny positive number (0.1 ns).
    rec_times = [max(t, 1e-7) for t in rec_times]
    iter_times = [max(t, 1e-7) for t in iter_times]

    # --- 2. Set up the Plot and Bar Positions ---
    x = np.arange(len(labels))  # Create numeric locations for each group of bars
    width = 0.35  # The width of each bar

    # Create the figure and axes objects, which are the canvas for our plot
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Create the two sets of bars, positioning them side-by-side
    rects1 = ax.bar(x - width/2, rec_times, width, label='Recursive')
    rects2 = ax.bar(x + width/2, iter_times, width, label='Iterative')

    # --- 3. Format the Axes and Labels ---
    # Set the y-axis to a logarithmic scale to handle exponential growth
    ax.set_yscale('log')
    # Apply our custom time_formatter to the y-axis ticks
    formatter = FuncFormatter(time_formatter)
    ax.yaxis.set_major_formatter(formatter)

    # Set the main labels for the chart
    ax.set_ylabel('Time (log scale)')
    ax.set_xlabel('Number of Disks')
    ax.set_title('Performance of Recursive vs. Iterative Solutions')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend() # Display the legend (Recursive/Iterative)

    # --- 4. Add Labels to the Bars ---
    # Generate custom labels for the top of each bar using our formatter
    rec_bar_labels = [time_formatter(t, None) for t in rec_times]
    iter_bar_labels = [time_formatter(t, None) for t in iter_times]
    ax.bar_label(rects1, labels=rec_bar_labels, padding=3, rotation=45)
    ax.bar_label(rects2, labels=iter_bar_labels, padding=3, rotation=45)

    # --- 5. Save the Figure ---
    # Adjust plot layout to prevent labels from being cut off
    fig.tight_layout()
    try:
        plt.savefig(graph_filename)
        print(f"Graph successfully saved.")
    except Exception as e:
        print(f"Error saving graph: {e}")
    finally:
        # Close the figure to free up memory
        plt.close(fig)



def process_and_write_results(input_file: str, output_file: str, display_moves_flag: bool, graph_flag: bool):
    """
    Main logic the entire puzzle-solving and reporting process.

    This function reads puzzle configurations from an input file, runs both
    the recursive and iterative solvers for each, times their performance,
    and writes a detailed report to an output file. It also coordinates the
    creation of a final summary table and a performance graph.

    Args:
        input_file (str): The path to the input file containing one integer
            (number of disks) per line.
        output_file (str): The path to the output file where the report will
            be written.
        display_moves_flag (bool): If True, the full list of moves will be
            included in the report for each puzzle.
        graph_flag (bool): If True, a .png graph of the results will be
            generated and saved.

    Side Effects:
        - Reads from the specified input file.
        - Creates and writes to the specified output file.
        - May create and save a .png image file in the same directory.
        - Prints status updates to the console.

    Returns:
        None
    """
    # This list will store timing results for the final summary and graph.
    all_timing_results = []
    
    print(f"Reading puzzles from '{input_file}'...")
    print(f"Writing results to '{output_file}'...")

    try:
        # Use a single 'with' block to manage both file handles safely.
        with open(output_file, 'w') as out_f, open(input_file, 'r') as in_f:
            for line in in_f:
                cleaned_line = line.strip()
                if not cleaned_line:  # Skip any blank lines in the input file
                    continue

                try:
                    num_disks = int(cleaned_line)

                    # Check for puzzle sizes that are too large to compute in a reasonable time.
                    if num_disks > 15:
                        warning_message = (
                            f"Warning: Skipping puzzle with {num_disks} disks. Due to exponential "
                            f"complexity (O(2^n)), solving for more than 15 disks can take an "
                            f"exceptionally long time. Please use a smaller value.\n"
                        )
                        out_f.write(warning_message)
                        out_f.write("\n" + "="*50 + "\n\n")
                        continue  # Move to the next line in the input file

                    out_f.write(f"Number of Disks: {num_disks}\n\n")

                    # --- Run and Time Both Solutions ---
                    # We create one puzzle object and reuse it for efficiency.
                    hanoi_puzzle = TowersOfHanoi(num_disks)
                    
                    start_rec = time.perf_counter()
                    hanoi_puzzle.solve_recursive()
                    duration_rec = time.perf_counter() - start_rec

                    # The verify_solution method returns a formatted report string.
                    recursive_verification_report = hanoi_puzzle.verify_solution(display_moves=display_moves_flag)
                    
                    # Reset the puzzle state before running the next solver.
                    hanoi_puzzle.reset()
                    
                    start_iter = time.perf_counter()
                    hanoi_puzzle.solve_iterative()
                    duration_iter = time.perf_counter() - start_iter

                    # The verify_solution method returns a formatted report string.
                    iterative_verification_report = hanoi_puzzle.verify_solution(display_moves=display_moves_flag)
                    
                    # Store results for the summary table and graph at the end.
                    all_timing_results.append({
                        "disks": num_disks,
                        "recursive_time": duration_rec,
                        "iterative_time": duration_iter
                    })
                    
                    # --- Write Report for this Puzzle ---
                    out_f.write("\n" + "--------Recursive Report--------- \n \n" + recursive_verification_report)
                    out_f.write("\n" + "--------Iterative Report--------- \n \n" + iterative_verification_report)
                    
                    # Write the timing metrics for this specific puzzle.
                    out_f.write(f"Recursive solution run time: {duration_rec:.6f} seconds\n")
                    out_f.write(f"Iterative solution run time: {duration_iter:.6f} seconds\n")
                    
                    # Write a separator for the next puzzle's report.
                    out_f.write("\n" + "="*50 + "\n\n")

                except ValueError:
                    # Handle lines in the input file that are not valid integers.
                    out_f.write(f"Skipping invalid line: '{cleaned_line}'\n")
                    out_f.write("="*50 + "\n\n")

            # --- Finalize Output After All Puzzles Are Processed ---
            if all_timing_results:
                write_summary_table(out_f, all_timing_results)
                
                if graph_flag:
                    # Derive graph filename from output filename (e.g., report.txt -> report.png)
                    base_filename = os.path.splitext(output_file)[0]
                    graph_filename = base_filename + '.png'
                    save_graph_image(all_timing_results, graph_filename)

    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return

    print("Processing complete.")