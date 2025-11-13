# Huffman Coding Lab

This program performs encoding and decoding of text phrases using Huffman coding. It is designed to run from the command line, read a structured input file, and generate three separate output files containing the results of its operations.

## File Structure

* `main.py`: The main entry point for the program.

* `processing_logic.py`: Contains all the core logic for parsing, processing, and generating files.

* `huffman_tree.py`: Contains the `HuffmanTree` class, which manages tree construction, encoding, and decoding.

* `frequency_table_generator.py`: Contains the logic for generating a frequency table from a text string.

* `priority_queue.py`: Implements the priority queue data structure.

* `tree.py`: Contains the base `Tree` class.

* `binary_tree.py`: Contains the `BinaryTree` class, which `HuffmanTree` inherits from.

* `node.py`: Contains the `Node` class used by the trees.

## How to Run

Run the program from your terminal using Python 3:

```
python main.py <input_file> [tree_file] [encode_file] [decode_file]
```

### Arguments

* `<input_file>`: **(Required)** The path to your structured input file.

* `[tree_file]`: **(Optional)** The name for the tree/map output file.

  * Defaults to: `tree_info.txt`

* `[encode_file]`: **(Optional)** The name for the encoding results file.

  * Defaults to: `encode_results.txt`

* `[decode_file]`: **(Optional)** The name for the decoding results file.

  * Defaults to: `decode_results.txt`

**Example:**
```
# Basic usage
python main.py my_tasks.txt

# Usage with custom output filenames
python main.py my_tasks.txt tree.txt encoding.txt decoding.txt
```

## Input File Format

The `<input_file>` must be a plain text file structured with up to three sections. Section headers are case-insensitive.

1. `FREQUENCY TABLE`: (Optional) A list of characters and their integer frequencies, one per line (e.g., `A 19`).

2. `ENCODE`: (Optional) A list of text phrases to be encoded, one per line.

3. `DECODE`: (Optional) A list of binary strings to be decoded, one per line.

**Example `input.txt`:**
```
FREQUENCY TABLE 
A 25 
B 10 
C 15 
D 30 
E 20

ENCODE 
ACE 
BAD 
BEE 
DEAD

DECODE 
1010110 
010001110
```

## How Logic is Handled

The program's behavior changes based on whether a `FREQUENCY TABLE` is provided in the input file.

### Encoding Logic

* **If a `FREQUENCY TABLE` is provided:** The program uses this single table to build one Huffman tree, and all phrases in the `ENCODE` section are encoded using that single tree.

* **If no `FREQUENCY TABLE` is provided:** The program generates a **new, unique** frequency table and Huffman tree for *each individual phrase* in the `ENCODE` section.

### Decoding Logic

* **If a `FREQUENCY TABLE` is provided:** The program uses this table to build a Huffman tree, and all binary strings in the `DECODE` section are decoded using that tree.

* **If no `FREQUENCY TABLE` is provided:** The program falls back to using the built-in **Standard Frequency Table** for all decoding tasks.

### `tree_info.txt` Report Logic

**This is important:** The `tree_info.txt` file (or your custom `[tree_file]`) **always shows the tree and encoding map that were used for the DECODING tasks.**

* If your input file has a `FREQUENCY TABLE`, `tree_info.txt` will show the tree built from **that table**.

* If your input file does **NOT** have a `FREQUENCY TABLE`, `tree_info.txt` will show the tree built from the **Standard Frequency Table**.

## Standard Frequency Table

This is the default, built-in table used for decoding when no other table is provided.

```
{ 
    "A": 19, "B": 16, "C": 17, "D": 11, "E": 42, "F": 12, 
    "G": 14, "H": 17, "I": 16, "J": 5, "K": 10, "L": 20, 
    "M": 19, "N": 24, "O": 18, "P": 13, "Q": 1, "R": 25, 
    "S": 35, "T": 25, "U": 15, "V": 5, "W": 21, "X": 2, 
    "Y": 8, "Z": 3 
}
```

## Output Files

The program generates three files:

1. **`tree_info.txt`**: Contains a visual representation of the Huffman tree and the complete character-to-code encoding map that was used for decoding.

2. **`encode_results.txt`**: Contains each original phrase from the `ENCODE` section followed by its encoded binary string.

3. **`decode_results.txt`**: Contains each original binary string from the `DECODE` section followed by its decoded text phrase.