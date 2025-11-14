def shell_sort(arr, increments):
    """
    Sorts 'arr' in-place using shell sort algorithm
    with a given sequence of increment. 

    Args:
        arr (list): The list of numbers to be sorted. 
        increments (list): The sequence of gap values to use, in ascending order (e.g., [1, 4, 8, ...])

    Returns: 
        None
    """
    # Loop through the increments, form largest to smallest
    for gap in reversed(increments):
        _insertion_sort_interleaved(arr, gap)

        

def _insertion_sort_interleaved(arr, gap):
    """
    Sorts interleaved elements of 'arr' using insertion sort with a specific 'gap'.
    This is the workhorse helper function for shell_sort. 

    Args:
        arr (list): The list to be sorted
        gap (int): The increment size defining the interleaved elements. 

    Returns: 
        None
    """
    # Start at the 'gap'-th element and go to the end.
    # By iterating i one by one (default step=1), we are essentially
    # processing all 'gap' number of interleaved sub-lists simultaneously
    # as we make a single pass over the array.
    for i in range(gap, len(arr)):
        # Store current value for insertion
        current_value = arr[i]
        position = i

        # Compare "backwards" by 'gap'
        while position >= gap and arr[position - gap] > current_value:
            # Shift the "gapped" element up
            arr[position] = arr[position - gap]

            # Move to the next "gapped" position
            position = position - gap
        
        # Place the current value in its correct sorted position
        arr[position] = current_value
