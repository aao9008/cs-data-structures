import sorting
import time 
import os 
import glob

# -- Helper: File I/O ---

def _read_data_file(filepath):
    """
    Reads a data file and returns a list of integer.
    Handles single or multiple numbers per line. 
    """

    # Empty list to hold numbers from input file
    data = []

    try:
        # Open file at filepath for reading
        with open(filepath, 'r') as f:
            # Read each line in the file
            for line in f:
                # For a line in file f, strip leading and trailing characters. 
                # For a line in file f, divide string into a list of substrings using the space character as a delimiter. 
                numbers_string = line.strip().split()

                # Iterate over each number string in the list of substrings
                for num_str in numbers_string:
                    # Convert the number string to an int and append to the data list
                    data.append(int(num_str))
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return None
    
    return data # data now contains all numbers from the file, and is ready for processing. 


def _write_results_header(file_handle, input_filename, data):
    """Helper to write original data to the results file"""
    file_handle.write(f"---Results for {input_filename} ---\n")
    file_handle.write("Original Data:\n")
    file_handle.write(f"{' '.join(map(str, data))}\n\n")

def _write_sorted_result(file_handle, sort_name, sorted_data):
    """Helper to write a single sorted array to the results file."""
    file_handle.write(f"Sorted by {sort_name}:\n")
    file_handle.write(f"{' '.join(map(str, sorted_data))}\n\n")


# --- Main Driver Function ---

def run_sorting_experiments(input_folder, output_dir = "sorted_results", timings_filepath = "timings_table.csv"):
    """
    Runs the full sorting lab, reading data files, timing sorts,
    and writing all results to output files.
    """
    print("Starting sorting experiments...")

    # --- Setup ---
    output_dir = "sorted_results"  # <-- New: Directory for sorted outputs
    timings_filepath = "timings_table.csv"
    
    # Create the output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Use glob to find all .dat and .txt files in the input folder
    input_files = glob.glob(os.path.join(input_folder, "*.dat")) + \
                  glob.glob(os.path.join(input_folder, "*.txt"))

    if not input_files:
        print(f"Error: No .dat or .txt files found in folder: {input_folder}")
        return

    # Number of times to run each sort for averaging (to avoid zero-time)
    RUNS_PER_TEST = 10 

    # --- Define Increment Sequences ---
    knuth_seq = [1, 4, 13, 40, 121, 364, 1093, 3280, 9841, 29524]
    seq_2 = [1, 5, 17, 53, 149, 373, 1123, 3371, 10111, 30341]
    seq_3 = [1, 10, 30, 60, 120, 360, 1080, 3240, 9720, 29160]
    my_seq = [1, 8, 23, 77, 263, 903, 3139, 10973] # Sedgewick's sequence

    # --- Define Sort Jobs ---
    sort_jobs = [
        {"name": "HeapSort", "func": sorting.heap_sort, "params": None},
        {"name": "ShellSort_Knuth", "func": sorting.shell_sort, "params": knuth_seq},
        {"name": "ShellSort_Seq2", "func": sorting.shell_sort, "params": seq_2},
        {"name": "ShellSort_Seq3", "func": sorting.shell_sort, "params": seq_3},
        {"name": "ShellSort_MySeq", "func": sorting.shell_sort, "params": my_seq},
    ]
    
    timing_results = [] # To store all timing data for the final table
    sort_names = [job['name'] for job in sort_jobs]

   # --- Main Loop: Process each file ---
    try:
        for filepath in input_files:
            filename = os.path.basename(filepath)
            print(f"Processing {filename}...")
            
            original_data = _read_data_file(filepath)
            if original_data is None:
                continue # Skip file if read error

            # --- Generate the new, specific output path ---
            name_part, _ = os.path.splitext(filename)
            results_filepath = os.path.join(output_dir, f"{name_part}_sorted.txt")
            
            file_timings = {"file": filename} # Dict to hold times for this file

            # Open the specific results file for this one input
            with open(results_filepath, 'w') as results_file:
                
                # Write the header and original data
                _write_results_header(results_file, filename, original_data)
                
                # Loop through each of the 5 sort algorithms
                for job in sort_jobs:
                    sort_name = job['name']
                    total_time = 0.0
                    sorted_data_for_output = [] 

                    # --- Branch is now OUTSIDE the timing loop ---
                    # We check *once* if this is a HeapSort or ShellSort job.
                    
                    if job['params'] is None:
                        # --- Timing Loop for HeapSort ---
                        for i in range(RUNS_PER_TEST):
                            data_copy = original_data.copy() 
                            
                            start_time = time.perf_counter()
                            job['func'](data_copy) 
                            end_time = time.perf_counter()
                            
                            total_time += (end_time - start_time)
                            if i == RUNS_PER_TEST - 1:
                                sorted_data_for_output = data_copy
                                
                    else:
                        # --- Timing Loop for ShellSort ---
                        # Get the params list once, before the loop
                        shell_increments = job['params']
                        for i in range(RUNS_PER_TEST):
                            data_copy = original_data.copy() 
                            
                            start_time = time.perf_counter()
                            job['func'](data_copy, shell_increments) 
                            end_time = time.perf_counter()
                            
                            total_time += (end_time - start_time)
                            if i == RUNS_PER_TEST - 1:
                                sorted_data_for_output = data_copy
                            
                    avg_time = total_time / RUNS_PER_TEST
                    
                    # Store time for the CSV table
                    file_timings[sort_name] = avg_time
                    
                    # Write sorted result to its specific file
                    _write_sorted_result(results_file, sort_name, sorted_data_for_output)

            # Add this file's timing data to the main list
            timing_results.append(file_timings)

        # --- After all files are processed, write the one timing table ---
        print(f"Writing timing table to {timings_filepath}...")
        with open(timings_filepath, 'w') as timings_file:
            # Write header
            timings_file.write(f"File,{','.join(sort_names)}\n")
            
            # Write data rows
            for row_data in timing_results:
                row_values = [row_data['file']]
                for name in sort_names:
                    row_values.append(f"{row_data.get(name, 0.0):.6e}")
                timings_file.write(f"{','.join(row_values)}\n")

    except IOError as e:
        print(f"Error opening or writing to output files: {e}")
        return
    except Exception as e:
        print(f"An unexpected error occurred during processing: {e}")
        return

    print("---")
    print("Experiments complete.")
    print(f"All sorted outputs saved in '{output_dir}/' directory.")
    print(f"Timing data saved to '{timings_filepath}'.")