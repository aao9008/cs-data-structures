from node import Node
from typing import Iterator

class BinaryTree:

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
    
    def root(self):
        """
        Public accessor for root node.
        
        Args:
            None
        
        Returns:
            The root node of the tree and None if tree is empty
        """

        return self._root
    

    def is_empty(self):
        """
        Checks if the tree contains any nodes
        
        Args: None
        
        Returns:
            bool: True if the tree is empty, False otherwise
        """

        return self._root is None
    

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

    def _count_nodes_recursive(self, node: Optional[Node]) -> int:
        """
        Private helper to recursively count nodes *only* for initialization.
        
        Args:
            node (Optional[Node]): The current node to start counting from.
        
        Returns:
            int: The count of nodes in the subtree rooted at 'node'.
        """
        if node is None:
            return 0
        
        # 1 (for the current node) + count of all nodes in left/right subtrees
        return 1 + self._count_nodes_recursive(node.left) + self._count_nodes_recursive(node.right)
    

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
            node (Optional[Node]): The current node to visit.
        """
        if node is not None:
            yield node  # 1. Visit Root
            yield from self._preorder_recursive(node.left)  # 2. Traverse Left
            yield from self._preorder_recursive(node.right) # 3. Traverse Right
    
    # --- Abstract Method ---
    
    def add(self, value) -> None:
        """
        Abstract method for adding a node.
        
        The generic BinaryTree does not know how to add nodes.
        A subclass (like a HuffmanTree) must implement this.
        
        Note: Our HuffmanTree will NOT use this, as it's built
        once via a different algorithm.
        """
        raise NotImplementedError('add method must be implemented by subclass')