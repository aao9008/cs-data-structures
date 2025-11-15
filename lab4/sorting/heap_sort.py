"""
Author: Alfredo Ormeno Zuniga
Date: 11/15/25

This file implements the iterative, in-place HeapSort
algorithm. It provides the main 'heap_sort' function
as well as its helper functions '_heapify' and
'_percolate_down'.
"""

def heap_sort(arr):
    """
    Sorts 'arr' in-place using the HeapSort algorithm. It first
    builds a max-heap, then repeatedly extracts the largest element 
    (swapping it to the end of the list) and re-heapifying the rest.

    Args:
        arr (list): The list of numbers to be sorted.

    Returns:
        None
    """
    # Get the size of the array
    n = len(arr)

    # Heapify the array
    _heapify(arr)

    # Loop from the last node to the second element
    for i in range(n - 1, 0, -1):

        # Swap the root (largest element) with the last element of the *current* heap at index i
        arr[0], arr[i] = arr[i], arr[0]

        # The heap is now smaller. Its new size is 'i'. 
        # Call _percolate_down on the new root (index 0) to fix heap property. 
        _percolate_down(arr, 0, i)


def _percolate_down(arr, node_index, arr_size):
    """
    Moves the node at 'node_index' down to its correct position
    in the max-heap. The heap is considered to be bounded by the array size.

    Args:
        arr (list): The list containing the heap.
        node_index (int): The index of the node to percolate down.
        arr_size (int): The exclusive upper bound of the heap (heap size).

    Returns:
        None
    """
    # Loop continues as long as we are percolating down
    while True:
        # Get indices of potential children
        child_0_index = 2 * node_index + 1
        child_1_index = 2 * node_index + 2

        #--- Stop Condition 1: Node is a leaf ---
        # if the left child is out of bounds, this node has no children
        if child_0_index >= arr_size:
            break

        # --- Find the index of the largest child ---
        # Check if the right child exists AND is larger than the left
        if child_1_index < arr_size and arr[child_1_index] > arr[child_0_index]:
            max_child = child_1_index
        # Left child is the larger child
        else:
            max_child = child_0_index

        # if child is bigger than parent -> swap values
        if arr[max_child] > arr[node_index]:
            arr[node_index], arr[max_child] = arr[max_child], arr[node_index]
            node_index = max_child   # continue percolating down
        # Parent node is larger than both children, max heap requirement is met. Exit loop. 
        else:
            break


def _heapify(arr):
    """
    Builds a max-heap from 'arr' in-place by percolating down
    all non-leaf nodes, starting from the last non-leaf node.

    Args:
        arr (list): The list to turn into a heap.

    Returns:
        None
    """
    # Identify internal node with the largest index: (N/2) - 1 
    n = len(arr)
    start_index = n // 2 - 1

    # Percolate down every non-leaf node in reverse order
    for node in range(start_index, -1, -1):
        _percolate_down(arr, node, n)
