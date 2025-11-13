"""
binary_tree.py

Author: Alfredo Ormeno Zuniga
Date: 10/27/25

Defines the BinaryTree class, a foundational concrete implementation of the abstract Tree.

This module provides the BinaryTree class, which serves as a base
structure for more specialized binary trees. It implements the core,
non-order-specific logic for a node-based binary tree, including
traversal, size calculation, and child-related methods.

It relies on the `Node` class for its structure and implements the
`Tree` abstract base class interface.
"""
from node import Node
from typing import Iterator
from tree import Tree

class BinaryTree(Tree):
    """
    A concrete implementation of the `Tree` abstract class for a binary tree.

    Provides common, non-order-specific binary tree functionality
    like traversals, child access, and O(1) size calculation.

    Attributes:
        _root (Optional[Node]): The root node of the tree.
        _size (int): The total number of nodes in the tree.
    """

    def __init__(self, root_node: Node = None):
        """
        Initializes a new binary tree

        Args: 
            root_node(optional Node): The node to set as the root. Defaults to None for an empty tree
        
        Returns: 
            None
        """
        self._root = root_node

        # Calculate size ONCE during initialization for efficient len()
        self._size = self._count_nodes_recursive(self._root)
    

    def _count_nodes_recursive(self, node):
        """
        Private helper to recursively count nodes *only* for initialization.
        
        Args:
            node (Node): The current node to start counting from.
        
        Returns:
            int: The count of nodes in the subtree rooted at 'node'.
        """
        if node is None:
            return 0
        
        # 1 (for the current node) + count of all nodes in left/right subtrees
        return 1 + self._count_nodes_recursive(node.left) + self._count_nodes_recursive(node.right)
    
    # --- Concrete Implementations of Abstract Methods from Tree---

    def root(self):
        """
        Public accessor for root node.
        
        Args:
            None
        
        Returns:
            The root node of the tree and None if tree is empty
        """

        return self._root
    

    def __len__(self) -> int:
        """
        Returns the total number of positions (nodes) in the tree.
        
        This enables the use of the built-in len(tree) function.
        This is an O(1) operation as the size is computed at init.

        Args:
            None
        
        Returns:
            int: The total count of nodes in the tree.
        """
        return self._size

    def num_children(self, node: Node) -> int:
        """
        Return the number of children that Node 'node' has.
        
        Args:
            node: current node
        
        Returns: 
            int: The total number of children that Node 'node' has. 
        """
        count = 0
        if node.left is not None:
            count += 1
        if node.right is not None:
            count += 1
        return count

    def children(self, node: Node) -> Iterator[Node]:
        """
        Generate an iteration of Nodes representing 'node's' children.

        Args: 
            node

        Returns:
            Iterator
        """
        if node.left is not None:
            yield node.left
        if node.right is not None:
            yield node.right
    

    # --- Methods that remain abstract (to be implemented by a subclass) ---

    def parent(self, node: Node):
        """
        Return the parent of Node 'node' (or None if 'node' is root).
        
        Note: This is an O(N) operation as it requires a traversal.
        A subclass could make this O(1) by adding parent pointers
        to the Node class. We leave it abstract.
        """
        raise NotImplementedError('parent method must be implemented by subclass')
    
    def add(self, value):
        """
        Abstract method for adding a value to the tree.
        (Inherited from Tree)
        """
        raise NotImplementedError('add method must be implemented by subclass')
    
    def remove(self, value):
        """
        Abstract method for removing a value from the tree.
        (Inherited from Tree)
        """
        raise NotImplementedError('remove method must be implemented by subclass')

    
    # --- Methods specific to BinaryTree ---
    

    def preorder_traversal(self) -> Iterator[Node]:
        """
        Generates an iteration of all nodes in the tree using preorder traversal.
        
        (Root, Left, Right)

        Args:
            None
        
        Returns:
            Iterator[Node]: An iterator that yields each Node in preorder.
        """
        yield from self._preorder_recursive(self._root)


    def _preorder_recursive(self, node):
        """
        Private helper to recursively yield nodes in preorder.

        Args:
            node (Node): The current node to visit.

        Returns:
            None
        """
        if node is not None:
            yield node  # 1. Visit Root
            yield from self._preorder_recursive(node.left)  # 2. Traverse Left
            yield from self._preorder_recursive(node.right) # 3. Traverse Right