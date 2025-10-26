# huffman_logic.py
"""
This module contains the core processing logic for the Huffman Coding lab.
It handles:
1. Parsing command-line arguments
2. Parsing the input file
3. Generating all output files (tree, encode, decode)
"""

import sys
from typing import Dict, List, Optional, Tuple
from huffman_tree import HuffmanTree
from frequency_table_generator import generate_frequency_table

# --- Orchestrator Function ---

def run_huffman_orchestrator(cli_args: List[str], standard_table: Dict[str, int]):
    """
    The main orchestrator that runs the entire lab process.
    
    This is called by the main script.

    Args:
        cli_args (List[str]): The command-line arguments (sys.argv).
        standard_table (Dict[str, int]): The fallback frequency table.
    """
    # 1. Parse command line arguments
    try:
        in_file, tree_file, encode_file, decode_file = parse_command_line_args(cli_args)
    except ValueError as e:
        print(f"Usage Error: {e}")
        print("Usage: python huffman_lab.py <input_file> [tree_file] [encode_file] [decode_file]")
        sys.exit(1)

    # 2. Parse the input file
    try:
        file_freq_table, phrases, codes = parse_input_file(in_file)
        print(f"Successfully parsed input file: {in_file}")
    except (FileNotFoundError, Exception) as e:
        print(f"Error reading input file: {e}")
        sys.exit(1)

    # 3. Set up the correct tree for decoding and reporting
    decoding_tree, table_name = setup_decoding_tree(file_freq_table, standard_table)
    
    # 4. Run all processing tasks
    generate_tree_report(decoding_tree, tree_file)
    process_encoding_tasks(phrases, file_freq_table, encode_file)
    process_decoding_tasks(codes, decoding_tree, table_name, decode_file)
    
    print("\nAll tasks complete.")

# --- File I/O Functions ---

def parse_command_line_args(args: List[str]) -> Tuple[str, str, str, str]:
    """
    Parses sys.argv into required file paths.
    
    Raises:
        ValueError: If the wrong number of arguments is provided.
        
    Returns:
        A tuple of (input_file, tree_file, encode_file, decode_file)
    """
    num_args = len(args)
    if num_args < 2 or num_args > 5:
        raise ValueError("Invalid number of arguments.")
    
    input_filepath = args[1]
    tree_filepath = args[2] if num_args >= 3 else "tree_info.txt"
    encode_filepath = args[3] if num_args >= 4 else "encode_results.txt"
    decode_filepath = args[4] if num_args == 5 else "decode_results.txt"
    
    return input_filepath, tree_filepath, encode_filepath, decode_filepath

def parse_input_file(filepath: str) -> Tuple[Dict[str, int], List[str], List[str]]:
    """
    Parses the structured input file into its three sections.
    (Moved from huffman_lab.py)
    """
    frequencies = {}
    phrases_to_encode = []
    codes_to_decode = []
    current_section = None
    
    with open(filepath, 'r') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            
            if line.upper() == "FREQUENCY TABLE":
                current_section = "freq"
            elif line.upper() == "ENCODE":
                current_section = "encode"
            elif line.upper() == "DECODE":
                current_section = "decode"
            elif current_section == "freq":
                parts = line.split()
                if len(parts) == 2 and parts[1].isdigit():
                    frequencies[parts[0].upper()] = int(parts[1])
            elif current_section == "encode":
                phrases_to_encode.append(line)
            elif current_section == "decode":
                codes_to_decode.append(line)
                    
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

# --- Core Logic Functions ---

def setup_decoding_tree(file_freq_table: Dict[str, int], 
                        standard_table: Dict[str, int]) -> Tuple[HuffmanTree, str]:
    """
    Determines which tree to use for decoding and reports.
    
    Returns:
        A tuple of (HuffmanTree, str) containing the
        correct tree and its descriptive name.
    """
    if file_freq_table:
        print("Found Frequency Table in file. Using it for reports and decoding.")
        tree = HuffmanTree(file_freq_table)
        name = "file's frequency table"
    else:
        print("No Frequency Table in file. Using standard table for reports and decoding.")
        tree = HuffmanTree(standard_table)
        name = "standard frequency table"
    return tree, name

def generate_tree_report(tree: HuffmanTree, output_filepath: str):
    """
    Generates the tree_info.txt content and writes it to a file.
    """
    print("Generating tree report...")
    content = ""
    content += "--- Huffman Tree Structure ---\n"
    content += tree.get_indented_tree_string()
    content += "\n\n--- Huffman Preorder Traversal String ---\n"
    content += tree.get_preorder_string()
    content += "\n\n--- Encoding Map ---\n"
    for char, code in tree.get_encoding_map().items():
        content += f"{char}: {code}\n"
    write_output_file(output_filepath, content)

def process_encoding_tasks(phrases: List[str], 
                           file_freq_table: Optional[Dict[str, int]], 
                           output_filepath: str):
    """
    Processes all encoding tasks and writes them to a file.
    """
    print("Processing encoding tasks...")
    encode_results = []
    
    if not file_freq_table:
        print(" -> Generating unique frequency table per phrase.")
        temp_tree = HuffmanTree()
        for phrase in phrases:
            phrase_freq_table = generate_frequency_table(phrase)
            temp_tree.construct_tree(phrase_freq_table)
            encoded_text = temp_tree.encode(phrase)
            encode_results.append(f"Original: {phrase}\nEncoded:  {encoded_text}\n(Used unique frequency table)")

            encode_results.append("\n--- Encoding Map ---")
            for char, code in temp_tree.get_encoding_map().items():
                encode_results.append(f"'{char}': {code}")
            encode_results.append("===================================END OF PHRASE===================================\n")
    else:
        print(" -> Using file's frequency table for all phrases.")
        encoding_tree = HuffmanTree(file_freq_table)
        for phrase in phrases:
            encoded_text = encoding_tree.encode(phrase)
            encode_results.append(f"Original: {phrase}\nEncoded:  {encoded_text}\n(Used file's frequency table)\n")

    write_output_file(output_filepath, "\n".join(encode_results))

def process_decoding_tasks(codes: List[str], 
                           decoding_tree: HuffmanTree, 
                           table_name: str, 
                           output_filepath: str):
    """
    Processes all decoding tasks using the provided tree and writes to a file.
    """
    print("Processing decoding tasks...")
    decode_results = []
    for code in codes:
        decoded_text = decoding_tree.decode(code)
        decode_results.append(f"Code:     {code}\nDecoded:  {decoded_text}\n(Used {table_name})\n")
    
    write_output_file(output_filepath, "\n".join(decode_results))