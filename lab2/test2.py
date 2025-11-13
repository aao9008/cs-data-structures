def build_fibonacci_tree(n):
    """
    Builds a Fibonacci binary tree of order n and returns the root node.

    Args:
        n (int): The order of the Fibonacci tree to build.

    Returns:
        Node: The root node of the generated tree, or None if n < 0.
    """
    # Handle invalid input
    if n < 0:
        return None

    # Base Case: For n=0 or n=1, the tree is a single node.
    if n == 0 or n == 1:
        return Node(n)

    # Recursive Step: For n > 1
    # Create a new root node for the current tree.
    root = Node(n)

    # Recursively build the left subtree with order n-1.
    root.left = build_fibonacci_tree(n - 1)

    # Recursively build the right subtree with order n-2.
    root.right = build_fibonacci_tree(n - 2)

    # Return the newly created root node.
    return root