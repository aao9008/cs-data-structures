import argparse
from reporting import process_and_write_results

def main():
    parser = argparse.ArgumentParser(description="Solve Towers of Hanoi and write results to a file.")
    parser.add_argument("input_file", help="Required: Path to the input file.")
    parser.add_argument("-o", "--output", default="output.txt", help="Optional: Path to the output file (default: output.txt).")
    parser.add_argument("-d", "--display", action="store_true", help="Optional: Flag to include the move list in the output file.")
    parser.add_argument("-g", "--graph", action="store_true", help="Optional: Flag to generate and append bar graph of the results.")
    
    args = parser.parse_args()

    process_and_write_results(args.input_file, args.output, args.display, args.graph)


if __name__ == "__main__":
    main()