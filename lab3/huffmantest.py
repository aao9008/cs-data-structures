"""
Huffman Coding Lab - Main Program

This program orchestrates the entire Huffman coding process.
It reads a specified input file, parses its contents, and performs
encoding and decoding based on the rules specified in the user request.

It generates three output files:
1.  tree_info.txt:   Contains the visual tree structure and encoding map.
2.  encode_results.txt: Contains the results of the encoding tasks.
3.  decode_results.txt: Contains the results of the decoding tasks.

To run:
    python huffman_lab.py path/to/your/input.txt
"""

import sys
from typing import Dict, List, Optional, Tuple

# Import from our other modules
from huffman_tree import HuffmanTree
from frequency_table_generator import generate_frequency_table

# --- Placeholder ---
# A standard frequency table for decoding if a frequency table is not provided in the input
STANDARD_FREQUENCY_TABLE = {
    "A": 19,"B": 16,"C": 17,"D": 11,"E": 42,"F": 12,
    "G": 14,"H": 17,"I": 16,"J": 5,"K": 10,"L": 20,
    "M": 19,"N": 24,"O": 18,"P": 13,"Q": 1,"R": 25,
    "S": 35,"T": 25,"U": 15,"V": 5,"W": 21,"X": 2,
    "Y": 8,"Z": 3,
}

def parse_input_file(filepath: str) -> Tuple[Dict[str, int], List[str], List[str]]:
    """
    Parses the structured input file into its three sections.

    Args:
        filepath (str): The path to the input file.

    Returns:
        A tuple containing:
        - (Dict[str, int]): The frequency table (empty if not found).
        - (List[str]): A list of phrases to encode.
        - (List[str]): A list of binary strings to decode.
    """
    frequencies = {}
    phrases_to_encode = []
    codes_to_decode = []
    
    current_section = None
    
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                
                # Check for section headers
                if line.upper() == "FREQUENCY TABLE":
                    current_section = "freq"
                elif line.upper() == "ENCODE":
                    current_section = "encode"
                elif line.upper() == "DECODE":
                    current_section = "decode"
                
                # Process the line based on the current section
                elif current_section == "freq":
                    parts = line.split()
                    if len(parts) == 2 and parts[1].isdigit():
                        frequencies[parts[0].upper()] = int(parts[1])
                elif current_section == "encode":
                    phrases_to_encode.append(line)
                elif current_section == "decode":
                    codes_to_decode.append(line)
                    
    except FileNotFoundError:
        print(f"Error: Input file not found at '{filepath}'")
        sys.exit(1)
    except Exception as e:
        print(f"Error parsing file: {e}")
        sys.exit(1)

    return frequencies, phrases_to_encode, codes_to_decode

def write_output_file(filename: str, content: str):
    """
    Helper function to write string content to a file.
    """
    try:
        with open(filename, 'w') as f:
            f.write(content)
        print(f"Successfully generated {filename}")
    except Exception as e:
        print(f"Error writing to {filename}: {e}")

def main():
    """
    Main execution function.
    """
    # 1. Get input file and optional output files from command-line arguments
    num_args = len(sys.argv)
    if num_args < 2 or num_args > 5:
        print("Usage: python huffman_lab.py <input_file> [tree_file] [encode_file] [decode_file]")
        print("  - <input_file> is required.")
        print("  - [tree_file], [encode_file], and [decode_file] are optional.")
        sys.exit(1)
        
    input_filepath = sys.argv[1]
    
    # 2. Define Output Filenames (set defaults, then override if provided)
    TREE_FILE = "tree_info.txt"
    ENCODE_FILE = "encode_results.txt"
    DECODE_FILE = "decode_results.txt"

    if num_args >= 3:
        TREE_FILE = sys.argv[2]
    if num_args >= 4:
        ENCODE_FILE = sys.argv[3]
    if num_args == 5:
        DECODE_FILE = sys.argv[4]

    # 3. Parse the input file
    print(f"Parsing input file: {input_filepath}...")
    file_freq_table, phrases_to_encode, codes_to_decode = parse_input_file(input_filepath)

    # 4. Handle Tree Report & Encoding Logic
    
    # We need a tree to generate the report.
    # If the file provided a table, we use that one.
    # If not, we'll use the standard table as a fallback for the report.
    tree_report_content = ""
    
    # This tree will be used for encoding if a table is provided
    encoding_tree = HuffmanTree() 
    
    if file_freq_table:
        print("Found Frequency Table in file. Using it for encoding and tree report.")
        encoding_tree.construct_tree(file_freq_table)
        tree_for_report = encoding_tree
    else:
        print("No Frequency Table in file. Using standard table for tree report.")
        # Create a tree from the standard table *just for the report*
        tree_for_report = HuffmanTree(STANDARD_FREQUENCY_TABLE)

    # Generate the tree report content
    tree_report_content += "--- Huffman Tree Structure ---\n"
    tree_report_content += tree_for_report.get_indented_tree_string()
    tree_report_content += "\n\n--- Encoding Map ---\n"
    for char, code in sorted(tree_for_report.get_encoding_map().items()):
        tree_report_content += f"{char}: {code}\n"
        
    # Write the tree report file
    write_output_file(TREE_FILE, tree_report_content)

    # 5. Process Encoding Tasks
    print("Processing encoding tasks...")
    encode_results = []
    if not file_freq_table:
        # Case: No frequency table given. Generate one per phrase.
        print("Generating unique frequency table per phrase for encoding...")
        temp_tree = HuffmanTree() # A reusable empty tree
        for phrase in phrases_to_encode:
            phrase_freq_table = generate_frequency_table(phrase)
            temp_tree.construct_tree(phrase_freq_table)
            encoded_text = temp_tree.encode(phrase)
            encode_results.append(f"Original: {phrase}\nEncoded:  {encoded_text}\n(Used unique frequency table)\n")
    else:
        # Case: Frequency table was given. Use the single encoding_tree.
        print("Using file's frequency table for all encoding tasks...")
        for phrase in phrases_to_encode:
            encoded_text = encoding_tree.encode(phrase)
            encode_results.append(f"Original: {phrase}\nEncoded:  {encoded_text}\n(Used file's frequency table)\n")

    write_output_file(ENCODE_FILE, "\n".join(encode_results))

    # 6. Process Decoding Tasks
    print("Processing decoding tasks...")
    # Use the same tree that was generated for the report.
    # This will be the file's tree if provided, or the standard table otherwise.
    decoding_tree = tree_for_report
    decode_results = []
    
    # Get the name of the table used for the report for clearer output
    table_name = "file's frequency table" if file_freq_table else "standard frequency table"

    for code in codes_to_decode:
        decoded_text = decoding_tree.decode(code)
        decode_results.append(f"Code:   {code}\nDecoded: {decoded_text}\n(Used {table_name})\n")
    
    write_output_file(DECODE_FILE, "\n".join(decode_results))

    print("\nAll tasks complete.")

if __name__ == "__main__":
    main()