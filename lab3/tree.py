"""
A general-purpose, abstract base class (ABC) for a Tree.

This module provides the base `Tree` class, which defines the
abstract interface that all tree structures should implement.
"""

from typing import Iterator
from abc import ABC, abstractmethod

class Tree(ABC):
    """
    Abstract base class representing a general tree structure.
    
    This class defines the methods that any concrete tree implementation
    must support, based on the ADT.
    """

    # --- Abstract methods that concrete subclasses MUST support ---
    def root(self):
        """
        Return the root Node of the tree (or None if empty).
        """
        raise NotImplementedError('must be implemented by subclass')

    @abstractmethod
    def parent(self, node: 'Node'):
        """
        Return the parent of Node 'node' (or None if 'node' is root).
        """
        raise NotImplementedError('must be implemented by subclass')

    @abstractmethod
    def num_children(self, node: 'Node') -> int:
        """
        Return the number of children that Node 'node' has.
        """
        raise NotImplementedError('must be implemented by subclass')

    @abstractmethod
    def children(self, node: 'Node') -> Iterator['Node']:
        """
        Generate an iteration of Nodes representing 'node's' children.
        """
        raise NotImplementedError('must be implemented by subclass')

    @abstractmethod
    def __len__(self) -> int:
        """
        Return the total number of elements (nodes) in the tree.
        """
        raise NotImplementedError('must be implemented by subclass')

    # --- Abstract methods for modification (optional for some trees) ---

    @abstractmethod
    def add(self, value) -> None:
        """
        Abstract method for adding a value to the tree.
        """
        raise NotImplementedError('add method must be implemented by subclass')
    
    @abstractmethod
    def remove(self, value) -> None:
        """
        Abstract method for removing a value from the tree.
        """
        raise NotImplementedError('remove method must be implemented by subclass')

    # --- Concrete methods that this class provides ---

    def is_root(self, node: 'Node') -> bool:
        """
        Return True if Node 'node' is the root of the tree.
        """
        return self.root() == node

    def is_leaf(self, node: 'Node') -> bool:
        """
        Return True if Node 'node' does not have any children.
        """
        return self.num_children(node) == 0

    def is_empty(self) -> bool:
        """
        Return True if the tree is empty.
        """
        return len(self) == 0