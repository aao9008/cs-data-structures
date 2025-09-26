"""Program Name: stack.py

A custom implementation of a stack data structure using a Python list.

This module defines the Stack class, which provides all standard LIFO
(Last-In, First-Out) operations such as push, pop, and peek. It also
includes a custom Empty exception for handling errors.

Author: Alfredo Ormeno Zuniga
Date: 09/11/2025
"""
class Stack:
    """
    Represents a last-in, first-out (LIFO) stack data structure.

    This implementation uses a Python list as the underlying container to
    store elements and provide standard stack operations.
    """

    def __init__(self):
        """Initializes an empty stack."""
        self.items = [] 


    def push(self, item):
        """
        Inserts an item to the top of the stack.

        Args:
            item (any type): The value to be added.

        Precondition:
            The stack is not full. (Note: Python lists grow dynamically).

        Postcondition:
            The stack has one more item, and the most recently added item
            is at the top.
        """
        # Python's list class is being used to implement a stack. 
        # Python's list class dynamically grows and shrinks in size, so there is no need to check of the stack is "full"

        # add an item to the top of the stack
        self.items += [item]


    def pop(self):
        """
        Removes the top element from the stack and returns it.

        Returns:
            A reference to the top item (the last value pushed).

        Raises: 
            Empty: If the stack is empty when the method is called.
        """
        # remove and return the top item from the stack
        # raise an error if the stack is empty
        if self.is_empty():
            raise Empty("stack is empty")
        
        # get the last item
        top_item = self.items[-1]

        # remove last item by slicing off the last element
        self.items = self.items[:-1]
        
        return top_item


    def peek(self):
        """
        Returns the top item without removing it from the stack.

        Returns:
            The item at the top of the stack.

        Raises: 
            Empty: If the stack is empty.
        """
        if self.is_empty():
            return None
        return self.items[-1]


    def is_empty(self):
        """
        Checks if the stack is empty.

        Returns:
            bool: True if the stack contains no items, False otherwise.
        """
        return len(self.items) == 0


    def size(self):
        """
        Returns the current number of items in the stack.

        Returns:
            int: The number of items in the stack.
        """
        return len(self.items)


class Empty(Exception):
    """Custom exception raised for operations on an empty stack."""
    pass
