# In sorting/__init__.py

"""
Sorting Package
Author: Alfredo Ormeno Zuniga
Date: 11/15/25

This package combines the sorting algorithms used in the lab,
making them available under a single 'sorting' namespace.
"""

# Import the main functions from their respective modules
from .heap_sort import heap_sort
from .shell_sort import shell_sort

# This list defines what 'from sorting import *' will import
__all__ = ['heap_sort', 'shell_sort']