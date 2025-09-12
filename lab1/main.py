from expression_converter import ExpressionConverter, InvalidExpressionError
import argparse
# Program Name: main.py
# Author: Alfredo Ormeno Zuniga
# Date: 09/11/2025
# Purpose:
#   This program serves as the driver for the Expression Converter project.
#   It reads arithmetic expressions from an input file, processes them using
#   the ExpressionConverter class, and writes the results to an output file.
#
# Functions:
#   - process_file(input_file, output_file): Reads expressions line by line,
#     determines the current category, performs the appropriate conversions,
#     and writes results or error messages to the output file.
#   - main(): Parses command-line arguments and calls process_file with the
#     specified input and output filenames.
#
def process_file(input_file, output_file):
    current_mode = None
    first_category = True

    with open(input_file, "r") as infile, open(output_file, "w") as outfile:
        for line in infile:
            line = line.strip()
            if not line:
                continue

            # Detect category headings
            if line.upper() in ["[INFIX]", "[PREFIX]", "[POSTFIX]"]:
                if not first_category:
                    outfile.write("\n")  # blank line before new category
                first_category = False
                current_mode = line.upper().strip("[]")
                outfile.write(f"{line}\n\n")  # heading + blank line
                continue

            # Process expressions depending on mode
            try:
                if current_mode == "INFIX":
                    outfile.write(f"Infix:   {line}\n")
                    prefix = ExpressionConverter.infix_to_prefix(line)
                    outfile.write(f"Prefix:  {prefix}\n\n")

                elif current_mode == "PREFIX":
                    outfile.write(f"Prefix:  {line}\n")
                    infix = ExpressionConverter.prefix_to_infix(line)
                    postfix = ExpressionConverter.prefix_to_postfix(line)
                    outfile.write(f"Infix:   {infix}\n")
                    outfile.write(f"Postfix: {postfix}\n\n")

                elif current_mode == "POSTFIX":
                    outfile.write(f"Postfix: {line}\n")
                    infix = ExpressionConverter.postfix_to_infix(line)
                    prefix = ExpressionConverter.postfix_to_prefix(line)
                    outfile.write(f"Infix:   {infix}\n")
                    outfile.write(f"Prefix:  {prefix}\n\n")

                else:
                    outfile.write(f"Error: No category specified before '{line}'\n\n")

            except InvalidExpressionError as e:
                outfile.write(f"Error: {e}\n\n")


def main():
    parser = argparse.ArgumentParser(description="Expression Converter")
    parser.add_argument("input", help="Input filename")
    parser.add_argument("output", nargs="?", default="output.txt", help="Output filename (default: output.txt)")
    args = parser.parse_args()

    process_file(args.input, args.output)

if __name__ == "__main__":
    main()