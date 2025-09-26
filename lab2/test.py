from towers_of_hanoi import TowersOfHanoi

def run_test(num_disks):
    """
    Initializes and runs an iterative test for the Towers of Hanoi puzzle.
    """
    print(f"--- Testing Iterative Solution for {num_disks} disks ---")

    # 1. Initialize the game
    hanoi_game = TowersOfHanoi(num_disks)

    # 2. Solve the puzzle
    moves_queue = hanoi_game.solve_iterative()

    # 3. Print the results
    move_count = 0
    while not moves_queue.is_empty():
        move_count += 1
        print(f"  {move_count}: {moves_queue.dequeue()}")

    # 4. Verify the number of moves
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
    run_test(5)
    
    # You can uncomment this to test with another value, like 4 disks.
    # run_test(4)