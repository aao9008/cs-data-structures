import time
import os
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter
import numpy as np
from towers_of_hanoi import TowersOfHanoi

def write_summary_table(file_handle, results_data):
    """Writes a formatted summary table of all timing results to the file."""
    file_handle.write("\n\n--- Performance Summary ---\n")
    # Write table header with clean formatting
    file_handle.write(f"{'Disks':<10} | {'Recursive Time (s)':<22} | {'Iterative Time (s)':<22}\n")
    file_handle.write(f"{'-'*10} | {'-'*22} | {'-'*22}\n")
    
    # Write a row for each result collected
    for result in results_data:
        disks = result['disks']
        rec_time = f"{result['recursive_time']:.6f}"
        iter_time = f"{result['iterative_time']:.6f}"
        file_handle.write(f"{disks:<10} | {rec_time:<22} | {iter_time:<22}\n")

def save_graph_image(results_data, graph_filename):
    """Saves a bar graph of the timing results to an image file using a log scale and dynamic units."""
    print(f"Generating and saving graph to '{graph_filename}'...")

    # Custom formatter for the y-axis ticks and bar labels
    def time_formatter(x, pos):
        if x >= 1:
            return f'{x:.2f} s'
        elif x >= 1e-3:
            return f'{x * 1e3:.2f} ms'
        else:
            return f'{x * 1e6:.2f} µs'

    labels = [result['disks'] for result in results_data]
    # Keep times in seconds for the formatter to work correctly
    rec_times = [result['recursive_time'] for result in results_data]
    iter_times = [result['iterative_time'] for result in results_data]

    # A log scale cannot plot zero. Replace any 0 values with a very small number.
    rec_times = [max(t, 1e-7) for t in rec_times]
    iter_times = [max(t, 1e-7) for t in iter_times]

    x = np.arange(len(labels))
    width = 0.35

    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width/2, rec_times, width, label='Recursive')
    rects2 = ax.bar(x + width/2, iter_times, width, label='Iterative')

    # --- THE FIX ---
    # 1. Set the y-axis to a logarithmic scale.
    ax.set_yscale('log')
    # 2. Apply the custom formatter for dynamic units (s, ms, µs).
    formatter = FuncFormatter(time_formatter)
    ax.yaxis.set_major_formatter(formatter)
    # 3. Update the y-axis label.
    ax.set_ylabel('Time (log scale)')
    # --- END FIX ---

    ax.set_xlabel('Number of Disks')
    ax.set_title('Performance of Recursive vs. Iterative Solutions')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    # Create custom labels for the bars using the same formatter logic
    rec_bar_labels = [time_formatter(t, None) for t in rec_times]
    iter_bar_labels = [time_formatter(t, None) for t in iter_times]
    ax.bar_label(rects1, labels=rec_bar_labels, padding=3, rotation=45)
    ax.bar_label(rects2, labels=iter_bar_labels, padding=3, rotation=45)

    fig.tight_layout()
    try:
        plt.savefig(graph_filename)
        print(f"Graph successfully saved.")
    except Exception as e:
        print(f"Error saving graph: {e}")
    finally:
        plt.close(fig)



def process_and_write_results(input_file, output_file, display_moves_flag, graph_flag):
    """
    Reads puzzles, times solutions, and writes formatted results and a summary table.
    """
    # This list will store timing results for the final summary table.
    all_timing_results = []
    
    print(f"Reading puzzles from '{input_file}'...")
    print(f"Writing results to '{output_file}'...")

    try:
        # Open both files at once to handle reading and writing
        with open(output_file, 'w') as out_f, open(input_file, 'r') as in_f:
            for line in in_f:
                cleaned_line = line.strip()
                if not cleaned_line:
                    continue

                try:
                    num_disks = int(cleaned_line)

                    if num_disks > 15:
                        # Write the warning message to output file
                        warning_message = (
                            f"Warning: Skipping puzzle with {num_disks} disks. Due to the exponential "
                            f"complexity (O(2^n)), solving for more than 15 disks can take an "
                            f"exceptionally long time. Please use a smaller value.\n"
                        )
                        out_f.write(warning_message)
                        out_f.write("\n" + "="*50 + "\n\n")
                        continue  # This skips the rest of the loop and goes to the next line

                    out_f.write(f"Number of Disks: {num_disks}\n\n")

                    # --- Time Recursive Solution ---
                    hanoi_puzzle = TowersOfHanoi(num_disks)
                    start_rec = time.perf_counter()
                    hanoi_puzzle.solve_recursive()
                    duration_rec = time.perf_counter() - start_rec

                    # --- Time Iterative Solution ---
                    hanoi_puzzle.reset()
                    start_iter = time.perf_counter()
                    hanoi_puzzle.solve_iterative()
                    duration_iter = time.perf_counter() - start_iter
                    
                    # Store results for the summary table at the end
                    all_timing_results.append({
                        "disks": num_disks,
                        "recursive_time": duration_rec,
                        "iterative_time": duration_iter
                    })
                    
                    # --- Generate and Write Report for this puzzle ---
                    verification_report = hanoi_puzzle.verify_solution(display_moves=display_moves_flag)
                    out_f.write(verification_report)
                    
                    # --- Write Timing Metrics for this puzzle ---
                    out_f.write(f"Recursive solution run time: {duration_rec:.6f} seconds\n")
                    out_f.write(f"Iterative solution run time: {duration_iter:.6f} seconds\n")
                    
                    # Separator for the next puzzle
                    out_f.write("\n" + "="*50 + "\n\n")

                except ValueError:
                    out_f.write(f"Skipping invalid line: '{cleaned_line}'\n")
                    out_f.write("="*50 + "\n\n")

            # After processing all puzzles, write the final summary table
            if all_timing_results:
                write_summary_table(out_f, all_timing_results)
                if graph_flag:
                    # Derive graph filename from output filename (e.g., output.txt -> output.png)
                    base_filename = os.path.splitext(output_file)[0]
                    graph_filename = base_filename + '.png'
                    save_graph_image(all_timing_results, graph_filename)


    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return

    print("Processing complete.")