from towers_of_hanoi import TowersOfHanoi

def run_iterative_test(num_disks):
    """
    Initializes and runs an iterative test for the Towers of Hanoi puzzle.
    """
    print(f"--- Testing Iterative Solution for {num_disks} disks ---")

    # 1. Initialize the game
    hanoi_game = TowersOfHanoi(num_disks)

    # 2. Solve the puzzle
    moves_queue = hanoi_game.solve_iterative()

    # 3. Print and verify the results
    verify_solution(moves_queue, num_disks)


def run_recursive_test(num_disks):
    """
    Initializes and runs a recursive test for the Towers of Hanoi puzzle.
    """
    print(f"--- Testing Recursive Solution for {num_disks} disks ---")

    # 1. Initialize the game
    hanoi_game = TowersOfHanoi(num_disks)

    # 2. Solve the puzzle
    moves_queue = hanoi_game.solve_recursive()

    # 3. Print and verify the results
    verify_solution(moves_queue, num_disks)


def verify_solution(moves_queue, num_disks):
    """
    Prints the moves from a queue and verifies the total count.
    """
    move_count = 0
    while not moves_queue.is_empty():
        move_count += 1
        print(f"  {move_count}: {moves_queue.dequeue()}")

    expected_moves = 2**num_disks - 1
    print(f"\nTotal moves: {move_count}")
    print(f"Expected moves: {expected_moves}")

    if move_count == expected_moves:
        print("Result: SUCCESS\n")
    else:
        print("Result: FAILED\n")


if __name__ == "__main__":
    # We'll test with n=3, as it's easy to verify manually.
    # The correct sequence for n=3 has 7 moves.
    test_disks = 25
    
    #run_iterative_test(test_disks)
    run_recursive_test(test_disks)