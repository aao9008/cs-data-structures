""""
node.py
Author: Alfredo Ormeno Zuniga
Date: 10/23/25

This module defines the 'Node' class for use in a
Huffman encoding tree.

It is intended to be imported by the main Huffman
algorithm script. The class's '__lt__' method
implements the custom comparison logic required for
the priority queue's tie-breaking rules.
"""

class Node:
    """
    Represents a node in the Huffman Tree.

    Nodes can be either leaf nodes (representing a single character) or
    internal nodes (representing a combination of child nodes). The
    comparison methods are implemented to support the specific
    tie-breaking rules for the Huffman priority queue.

    Attributes:
        symbol (str): The character (e.g., 'A') or combined symbols (e.g., 'AZ')
                      represented by this node.
        weight (int | float): The frequency or combined frequency of the symbol(s).
        left (Optional[Node]): The left child node. None for leaf nodes.
        right (Optional[Node]): The right child node. None for leaf nodes.
        parent (Optional[Node]): The parent node. None for root
    """
    def __init__(self, symbol: str, weight: int):
        """
        Initializes a new Node.

        Args:
            symbol (str): The character or combined symbols.
            weight (int | float): The frequency of the symbol(s).
        
        Returns: 
            None
        """
        self.symbol = symbol
        self.weight = weight
        self.left = None
        self.right = None
        self.parent = None


    def __lt__(self, other: 'Node') -> bool:
        """
        Defines the 'less-than' comparison for two Node objects.

        This method is used directly by `heapq` (min-heap) to determine
        priority. It implements the lab's specific tie-breaking rules.

        Args:
            other (Node): The other Node object to compare against.

        Returns:
            bool: True if this node has higher priority (is "less than")
                  the other node, False otherwise.
        """
        # 1. Primary sort: Lowest weight wins
        if self.weight != other.weight:
            return self.weight < other.weight

        # 2. Tie-breaker 1: Single-letter vs. Multi-letter
        self_is_single = (len(self.symbol) == 1)
        other_is_single = (len(other.symbol) == 1)

        if self_is_single != other_is_single:
            # `True` (is single) is "less than" `False` (is multi),
            # so this gives precedence to the single-letter node.
            return self_is_single > other_is_single

        # 3. Tie-breaker 2: Alphabetical
        return self.symbol < other.symbol
    

    def __repr__(self) -> str:
        """
        Returns an unambiguous string representation of the Node.

        Returns:
            str: A string in the format '(SYMBOL: WEIGHT)'.
        """
        return f"({self.symbol}: {self.weight})"