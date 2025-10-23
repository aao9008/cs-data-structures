""""
This module provides the HuffmanTree class, which inherits from
BinaryTree and provides all the specific logic for:
1.  Building the tree from a frequency table.
2.  Generating an encoding map (e.g., {'A': '01'}).
3.  Encoding text to a binary string.
4.  Decoding a binary string back to text.
"""

from binary_tree import BinaryTree
from priority_queue import PriorityQueue
from node import Node
from typing import Dict

class HuffmanTree(BinaryTree):
    """
    A specific implementation of a BinaryTree for Huffman coding.

    This class orchestrates the entire process:
    - Builds the tree from a frequency table using a PriorityQueue.
    - Generates the character-to-binary-code map.
    - Provides public methods to encode and decode text.
    """

    def __init__(self, frequency_table: Dict[str, int]):
        """
        Initializes a new Huffman Tree by building it from a frequency table.

        This method overrides the parent __init__ and runs the full
        Huffman algorithm.

        Args:
            frequency_table (Dict[str, int]): A dictionary mapping
                characters to their frequencies (e.g., {'A': 19, 'B': 16}).
        """
        self._encoding_map: Dict[str, str] = {}
        
        if not frequency_table:
            super().__init__(None)  # Initialize parent with an empty tree
            return

        # Encapsulate the build logic into a private method
        root_node = self._build_tree(frequency_table)

        # Initialize the parent BinaryTree with the completed root
        super().__init__(root_node) 

        # Build the encoding map (e.g., {'A': '010'})
        self._build_encoding_map_recursive(self._root, "")

    def _build_tree(self, frequency_table: Dict[str, int]) -> Optional[Node]:
        """
        Private helper to build the Huffman tree structure.
        
        Uses the core algorithm with a PriorityQueue to construct
        the tree from the bottom up.

        Args:
            frequency_table (Dict[str, int]): A mapping of characters
                                              to their frequencies.
        
        Returns:
            Optional[Node]: The root node of the fully constructed tree.
        """
        pq = PriorityQueue()
        for symbol, weight in frequency_table.items():
            pq.push(Node(symbol, weight))

        # Core Huffman Algorithm:
        # Loop until only one node remains in the queue (the root).
        while pq.size() > 1:
            # 1. Pop the two nodes with the highest priority (lowest weight)
            left_node = pq.pop()
            right_node = pq.pop()

            # 2. Combine them into a new internal node
            #    Sort the symbol string for consistent tie-breaking
            new_symbol = "".join(sorted(left_node.symbol + right_node.symbol))
            new_weight = left_node.weight + right_node.weight
            
            parent_node = Node(new_symbol, new_weight)
            parent_node.left = left_node
            parent_node.right = right_node
            
            # 3. Add the new internal node back into the queue
            pq.push(parent_node)
        
        # The last node in the queue is the root of the tree
        root_node: Optional[Node] = None
        if not pq.is_empty():
            root_node = pq.pop()
        
        return root_node

    def _build_encoding_map_recursive(self, node, code_so_far: str):
        """
        Private helper to recursively build the encoding map.
        Uses a preorder traversal to find leaf nodes and their paths.

        Args:
            node (Optional[Node]): The current node in the traversal.
            code_so_far (str): The binary string accumulated from the
                               root to this node.
        """
        if node is None:
            return
        
        # Base case: A leaf node (it has a character symbol)
        if node.left is None and node.right is None:
            # Handle edge case: tree has only one node (e.g., "AAAAA")
            # Assign '0' as its code.
            if code_so_far == "":
                self._encoding_map[node.symbol] = "0"
            else:
                self._encoding_map[node.symbol] = code_so_far
            return
        
        # Recursive step: An internal node.
        # Go left, appending '0' to the path
        self._build_encoding_map_recursive(node.left, code_so_far + "0")
        # Go right, appending '1' to the path
        self._build_encoding_map_recursive(node.right, code_so_far + "1")

    def get_encoding_map(self) -> Dict[str, str]:
        """
        Public accessor for the encoding map.

        Returns:
            Dict[str, str]: A *copy* of the character-to-code mapping.
        """
        return self._encoding_map.copy()

    def get_preorder_string(self) -> str:
        """
        Generates the string representation of the preorder traversal
        as required by the lab.

        Returns:
            str: A formatted string of nodes in preorder
                 (e.g., "XYZ:6, X:3, YZ:3, Y:1, Z:2").
        """
        nodes_str = []
        # We use the 'preorder_traversal' method inherited from BinaryTree!
        for node in self.preorder_traversal():
            nodes_str.append(f"{node.symbol}: {node.weight}")
        
        return ", ".join(nodes_str)

    def encode(self, text: str) -> str:
        """
        Encodes a given string into its Huffman binary representation.
        
        As per lab spec, this method ignores punctuation, spaces,
        and is case-insensitive (treats 'a' as 'A').

        Args:
            text (str): The input string to encode (e.g., "Sally sells...").
        
        Returns:
            str: The resulting binary code string (e.g., "0101100...").
        """
        encoded_string = []
        for char in text:
            # Check if it's an alphabet character
            if char.isalpha():
                # Convert to uppercase and get its code
                code = self._encoding_map.get(char.upper())
                
                # Append the code if the character is in our map
                if code:
                    encoded_string.append(code)
                # If not in map (e.g. char from a different language), ignore it.
        
        return "".join(encoded_string)

    def decode(self, encoded_text: str) -> str:
        """
        Decodes a Huffman binary string back into the original text.

        Args:
            encoded_text (str): The binary code string to decode.
        
        Returns:
            str: The decoded text (e.g., "SALLYSELLS...").
        """
        # If tree is empty, cannot decode.
        if self.is_empty():
            return ""
            
        decoded_string = []
        current_node = self._root # Start at the root

        for bit in encoded_text:
            if current_node is None:
                # Should not happen if code is valid, but good for safety
                break 
                
            # 1. Follow the path
            if bit == '0':
                current_node = current_node.left
            elif bit == '1':
                current_node = current_node.right
            
            # 2. Check if we landed on a leaf
            if current_node is not None and current_node.left is None and current_node.right is None:
                # We found a character!
                decoded_string.append(current_node.symbol)
                # Go back to the root to find the next character
                current_node = self._root
        
        return "".join(decoded_string)