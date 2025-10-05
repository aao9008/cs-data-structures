# Towers of Hanoi Performance Analyzer

## Overview

This program analyzes the performance of two different algorithms for solving the Towers of Hanoi puzzle: a recursive solution and a iterative solution.

It reads a list of puzzle sizes (number of disks) from an input file, runs both solvers for each size, and measures the execution time. The results, including verification of the number of moves and detailed performance metrics, are saved to a text file. Optionally, a graphical bar chart comparing the run times can be generated.

## Features

* Solves the Towers of Hanoi puzzle using both recursive and iterative methods.
* Accurately times the performance of each algorithm.
* Processes multiple puzzle sizes from a single input file.
* Generates a detailed text report with timing data and move verification.
* Optionally includes the full list of moves in the report.
* Optionally generates a `.png` bar chart visualizing the performance results on a logarithmic scale.

## Requirements

This project has a few external dependencies, all of which are listed in the `requirements.txt` file.
* `numpy`
* `matplotlib`

## Setup Instructions

To ensure the program runs correctly, it is highly recommended to use a Python virtual environment.

1.  **Create a Virtual Environment:**
    Open your terminal in the project directory and run:
    ```sh
    python -m venv venv
    ```

2.  **Activate the Environment:**
    * **On macOS/Linux:**
        ```sh
        source venv/bin/activate
        ```
    * **On Windows:**
        ```sh
        venv\Scripts\activate
        ```

3.  **Install Required Packages:**
    With the virtual environment active, install all dependencies from the `requirements.txt` file using pip:
    ```sh
    pip install -r requirements.txt
    ```

## How to Use

The program is run from the command line and accepts several arguments to control its behavior.

### Basic Syntax
```sh
python main.py <input_file> [options]
```

### Command-Line Arguments

* **`input_file`** (Required)
    * The path to the input text file.
    * This file should contain one integer per line, representing the number of disks for each puzzle.
    * Blank lines are ignored.
    * **Note:** It has been determined that puzzle sizes (`n`) greater than 15 may take an exceptionally long time to solve on most personal computers due to the exponential nature of the problem (O(2^n)). It is recommended to use values of 15 or less.

* **`-o, --output <filename>`** (Optional)
    * Specifies the name for the output report file.
    * If not provided, it defaults to `output.txt`.

* **`-d, --display`** (Optional)
    * A flag to include the complete, step-by-step list of moves in the output report. It's recommended you only display moves for n values of 10 or less. 

* **`-g, --graph`** (Optional)
    * A flag to generate and save a `.png` bar chart that visually compares the performance of the two algorithms. The image will be saved with the same base name as the output file.

### Example Usage

1.  **Basic run with default output:**
    ```sh
    python main.py puzzles.txt
    ```
    *(This will create `output.txt`)*

2.  **Specify an output file and include the moves list:**
    ```sh
    python main.py puzzles.txt --output report.txt --display
    ```
    *(This will create `report.txt` with the full move list)*

3.  **Generate the report and the performance graph:**
    ```sh
    python main.py puzzles.txt -o results.txt -g
    ```
    *(This will create `results.txt` and `results.png`)*

## Output Files

The program will generate one or two files based on the arguments provided:

1.  **Report File (`.txt`):** A detailed text file containing the verification, move counts, and timing results for each puzzle size.
2.  **Graph Image (`.png`):** (Optional) A bar chart visualizing the run times, saved as a PNG image.