"""
A test script for the priority_queue module.

This script verifies that the PriorityQueue correctly orders Node objects
based on the three specified rules:
1.  Lowest weight first.
2.  Single-letter nodes before multi-letter nodes (on tie).
3.  Alphabetical order (on further tie).
"""

from priority_queue import PriorityQueue
from node import Node

def run_tests():
    """Runs a suite of tests on the PriorityQueue."""

    print("--- Running Priority Queue Test ---")

    # 1. Define a list of nodes designed to test all sorting rules.
    nodes_to_test = [
        Node('Z', 20),          # A standard, higher-weight node.
        Node('A', 10),          # A standard, lower-weight node.
        Node('V', 15),          # Will tie on weight and type with 'J'.
        Node('J', 15),          # Should come before 'V' alphabetically.
        Node('MULTI', 15),      # Will tie on weight with 'J' and 'V'.
        Node('Zebra', 15),      # New multi-node to test alphabetical tie-break.
        Node('Apple', 15),      # New multi-node to test alphabetical tie-break.
        Node('B', 10)           # Will tie on weight and type with 'A'.
    ]

    # 2. Define the expected order of retrieval from the queue.
    #    This is based on manual application of the priority rules.
    expected_order = [
        "(A: 10)",      # Lowest weight is 10. 'A' comes before 'B'.
        "(B: 10)",      #
        "(J: 15)",      # Next weight is 15. Singles before Multis. 'J' before 'V'.
        "(V: 15)",      #
        "(Apple: 15)",  # Multi-nodes are sorted alphabetically.
        "(MULTI: 15)",  #
        "(Zebra: 15)",  #
        "(Z: 20)"       # Highest weight comes last.
    ]

    # 3. Create and populate the priority queue.
    pq = PriorityQueue()
    print("\nPushing nodes onto the queue...")
    for node in nodes_to_test:
        print(f"  Pushing {node}...")
        pq.push(node)

    # 4. Pop nodes from the queue and record their order.
    actual_order = []
    print("\nPopping nodes from the queue...")
    while not pq.is_empty():
        popped_node = pq.pop()
        print(f"  Popped {popped_node}")
        actual_order.append(str(popped_node))

    # 5. Compare the actual order to the expected order.
    print("\n--- Test Results ---")
    print(f"Expected Order: {expected_order}")
    print(f"Actual Order:   {actual_order}")

    if actual_order == expected_order:
        print("\n SUCCESS: The PriorityQueue ordering is correct!")
    else:
        print("\n FAILURE: The PriorityQueue ordering is incorrect.")

if __name__ == "__main__":
    run_tests()
