"""
AI-Generated Module for Huffman Priority Queue.
AI Model: Google Gemini

This module provides a PriorityQueue class tailored
for building a Huffman Encoding Tree.

The sorting logic for the queue is:
1.  Lowest weight has the highest priority.
2.  If weights are tied, a single-letter node has priority over
    a multi-letter node.
3.  If both weights and types are tied, nodes are sorted alphabetically
    by their symbol.
"""

import heapq
from typing import Optional
from node import Node

class PriorityQueue:
    """
    A min-priority queue wrapper for the `heapq` module.

    This queue stores `Node` objects and uses their built-in
    comparison method (`__lt__`) to maintain heap order.
    """

    def __init__(self):
        """Initializes an empty priority queue."""
        self._heap: list[Node] = []


    def push(self, node: Node):
        """
        Pushes a Node onto the priority queue.

        The queue's order will be automatically maintained based on
        the Node's `__lt__` method.

        Args:
            node (Node): The Node object to add to the queue.

        Returns:
            None
        """
        heapq.heappush(self._heap, node)


    def pop(self) -> Optional[Node]:
        """
        Pops and returns the Node with the highest priority (lowest value).

        Returns:
            Optional[Node]: The highest-priority Node, or None if the
                            queue is empty.
        """
        if not self.is_empty():
            return heapq.heappop(self._heap)
        return None
    

    def is_empty(self) -> bool:
        """
        Checks if the priority queue is empty.

        Returns:
            bool: True if the queue is empty, False otherwise.
        """
        return len(self._heap) == 0
    

    def size(self) -> int:
        """
        Returns the number of items in the priority queue.

        Returns:
            int: The count of nodes currently in the queue.
        """
        return len(self._heap)