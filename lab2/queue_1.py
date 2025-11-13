"""A high-performance implementation of a queue data structure.

This module defines the Queue class using a circular array, which provides
amortized O(1) time complexity for both enqueue and dequeue operations.
It imports the custom Empty exception from the stack module.

Author: Alfredo Ormeno Zuniga
Date: 09/26/2025
"""
# Import the custom exception from your stack module
from stack import Empty

class Queue:
    """
    Represents a first-in, first-out (FIFO) queue data structure.

    This implementation uses a circular array with dynamic resizing,
    achieving O(1) amortized cost for enqueue and dequeue operations.
    """
    DEFAULT_CAPACITY = 10

    def __init__(self):
        """Initializes an empty queue."""
        self._data = [None] * Queue.DEFAULT_CAPACITY
        self._size = 0
        self._front = 0

    def _resize(self, cap):
        """
        Resizes the internal array to a new capacity.

        This utility method copies all existing elements from the old
        circular array into a new, linear array of the specified capacity.

        Args:
            cap (int): The new capacity for the internal array.
        
        Returns: 
            None
        """
        old = self._data # Save a reference to the current list

        self._data = [None] * cap # Change the queue's current list to a new empty list with an new capacity. 

        walk = self._front # Variable to be used to traverse the old list

        # Loop through the existing elements and copy them to the new list
        for i in range(self._size): 
            
            self._data[i] = old[walk] 

            walk = (1 + walk) % len(old) # Use old length for modulo to correctly wrap around
        
        # After copying, the front of the queue is reset to index 0  
        self._front = 0

    def is_empty(self):
        """
        Checks whether the queue has no items.

        Returns:
            bool: True if the queue contains no items, False otherwise.
        """
        return self._size == 0

    def enqueue(self, item):
        """
        Adds an item to the back of the queue.

        Args:
            item (any type): The value to be added.
        
        Returns:
            None
        """
        # If the array is full, double its capacity.
        if self._size == len(self._data):
            self._resize(2 * len(self._data))
        
        # Calculate the next available index in a circular fashion.
        avail = (self._front + self._size) % len(self._data)
        self._data[avail] = item
        self._size += 1

    def dequeue(self):
        """
        Removes and returns the item from the front of the queue.

        The item that was added first will be the first one removed.

        Returns:
            The front item in the queue.

        Raises:
            Empty: If the queue is empty.
        """
        if self.is_empty():
            raise Empty("Queue is empty")
        
        answer = self._data[self._front]
        self._data[self._front] = None  # Help with garbage collection.
        self._front = (self._front + 1) % len(self._data)
        self._size -= 1

        # If the number of items is less than a quarter of the capacity,
        # shrink the array to half its size to save memory.
        if 0 < self._size < len(self._data) // 4:
            self._resize(len(self._data) // 2)

        return answer

    def first(self):
        """
        Returns the front item of the queue without removing it.

        Returns:
            The front item in the queue.

        Raises:
            Empty: If the queue is empty.
        """
        if self.is_empty():
            raise Empty("Queue is empty")
        return self._data[self._front]

    def size(self):
        """
        Returns the current number of items in the queue.

        Returns:
            int: The number of items in the queue.
        """
        return self._size