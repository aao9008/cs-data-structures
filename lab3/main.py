"""
main.py
Author: Alfredo Ormeno Zuniga
Date: 10/27/25

This program orchestrates the entire Huffman coding process.
It acts as the single entry point, passing command-line arguments
and global configuration to the huffman_logic module.
"""

import sys
from processing_logic import run_huffman_orchestrator


# Frequency table to be used, if one is not provided as part of the input. 
STANDARD_FREQUENCY_TABLE = {
    "A": 19,"B": 16,"C": 17,"D": 11,"E": 42,"F": 12,
    "G": 14,"H": 17,"I": 16,"J": 5,"K": 10,"L": 20,
    "M": 19,"N": 24,"O": 18,"P": 13,"Q": 1,"R": 25,
    "S": 35,"T": 25,"U": 15,"V": 5,"W": 21,"X": 2,
    "Y": 8,"Z": 3,
}

def main():
    """
    Main execution function.
    
    Passes command-line arguments and the standard table to
    the logic orchestrator.
    """
    run_huffman_orchestrator(sys.argv, STANDARD_FREQUENCY_TABLE)

if __name__ == "__main__":
    main()