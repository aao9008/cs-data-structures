# Program Name: stack.py
# Author: Alfredo Ormeno Zuniga
# Date: 09/11/2025
# Purpose:
#   This module provides a custom implementation of a stack data structure
#   using Python’s built-in list type as the underlying container.
#
# Functions:
#   - push(item):      Adds an item to the top of the stack.
#   - pop():           Removes and returns the item at the top of the stack.
#                      Raises an Empty exception if the stack is empty.
#   - peek():          Returns the top item without removing it from the stack.
#   - isEmpty():       Returns True if the stack contains no items, False otherwise.
#   - size():          Returns the current number of items in the stack.
#
class Stack:
    def __init__(self):
        # Initialize an empty list to store stack items
        self.items = [] 
    
    # Function: push
    # Purpose: Insert an item to the top of the stack 
    # Input: item (any type) - the value to be added
    # Precondition: The stack is not full
    # Postcondition: The stack has one more item and the most recently added item is at the top
    # Output: none
    def push(self, item):
        # Python's list class is being used to implement a stack. 
        # Python's list class dynamically grows and shrinks in size, so there is no need to check of the stack is "full"

        # add an item to the top of the stack
        self.items += [item]
    # END push

    # Function: pop
    # Purpose: Remove the top element from the stack and return to user
    # Input: none
    # Precondition: The stack should not be empty
    # Postcondition: The most recently push item on the stack has been removed and the stack now has 1 less element
    # Output: A reference to the top item (the last value pushed)
    def pop(self):
        # remove and return the top item from the stack
        # raise an error if the stack is empty
        if self.isEmpty():
            raise Empty("stack is empty")
        
        # get the last item
        top_item = self.items[-1]
        # remove last item by slicing off the last element
        self.items = self.items[:-1]
        
        return top_item
    # END pop

    # Function: peek
    # Purpose: Return the top item without removing it
    # Input: None
    # Precondition: The stack may be empty
    # Postcondition: Stack remains unchanged
    # Output: The top item if the stack is not empty, 
    #         otherwise None
    def peek(self):
        if self.isEmpty():
            return None
        return self.items[-1]
    # END peek

    # Function: is_empty
    # Purpose: Check whether the stack has no items
    # Input: None
    # Precondition: Stack has been initialized
    # Postcondition: Stack remains unchanged
    # Output: Boolean value 
    #         - True if the stack contains no items
    #         - False if the stack contains one or more items
    def isEmpty(self):
        return len(self.items) == 0
    # END isEmpty

    def size(self):
        return len(self.items)
    # END len
# END Stack

# Class: Empty
# Purpose: Define a custom exception that is raised when 
#          attempting to access or remove an element from an empty stack.
# Attributes: None
# Methods: None
class Empty(Exception):
    """Error attempting to access an element from an empty container."""
    pass
# END Empty