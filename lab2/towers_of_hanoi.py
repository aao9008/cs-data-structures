"""This module provides a comprehensive solution to the Towers of Hanoi puzzle.

It contains a primary class, TowersOfHani, which encapsulates the game state
and provides methods for both iterative and recursive solutions. 

This module also includes helper data structures (Stack and Queue) for its operation.

Author: Alfredo Ormeno Zuniga
Date: 09/26/2025
"""
from stack import Stack
from queue_1 import Queue

class TowersOfHanoi:
    """
    Represents and solves a single instance of a Towers of Hanoi puzzle.

    This class encapsulates the state of a Towers of Hanoi game, including the
    three pegs (source, auxiliary, target) and the number of disks. It provides
    methods to solve the puzzle using both iterative and recursive algorithms.

    Attributes:
        num_disks (int): The number of disks in the puzzle.
        source (Stack): The starting peg, initialized with all the disks.
        aux (Stack): The auxiliary peg.
        target (Stack): The destination peg.
        moves (Queue): A queue to store the sequence of move descriptions.
        smallest_disk_location (str): Tracks the current peg of disk 1.
        move_number (int): A counter for the current move number.
    """

    def __init__(self, n):
        """
        Initialize all game pieces for a new Towers of Hanoi Puzzle 
        """
        self.num_disks = n
        self.source = Stack()
        self.aux = Stack()
        self.target = Stack()
        self.moves = Queue()
        self.smallest_disk_location = "source"
        self.move_number = 1

        self.initialize_source_peg()



    def reset(self, num_disks = None):
        """
        Resets the puzzle to its initial state

         This method re-initializes all puzzle components, including the pegs,
        the moves queue, and the state trackers. It can be used to either
        restart the puzzle with a new number of disks or to simply reset the
        current puzzle to its starting configuration.

        Args:
            num_disks (int, optional): The number of disks for the reset puzzle.
                If not provided or None, the puzzle is reset using the current
                `self.num_disks` value. Defaults to None.  

        Returns: 
            None
        """
        if num_disks is None: 
            # User did not provide a new value, so use the existing one. 
            num_disks = self.num_disks

        # Reset the game object's state using determined num_disks.
        self.num_disks = num_disks
        self.source = Stack()
        self.aux = Stack()
        self.target = Stack()
        self.moves = Queue()
        self.smallest_disk_location = "source"
        self.move_number = 1
        

        self.initialize_source_peg()



    def initialize_source_peg(self):
        """
        Initializes the source peg with all the disks.

        This method populates the source stack by pushing disks
        numbered from `self.num_disks` down to 1. This process ensures that
        the largest disk is at the bottom of the stack and the smallest is at
        the top, representing the correct starting configuration for the Towers of Hanoi puzzle.
        """

        # Load disks onto the source peg from largest to smallest
        for i in range(self.num_disks, 0, -1):
            self.source.push(i)


    def _format_moves_string(self):
        """Formats the moves queue into a multi-line, human-readable string.

        This is a non-destructive helper method that reads the contents of the
        `self.moves` queue and formats them into a numbered list. It carefully
        preserves the original queue by using a temporary queue to store and
        then restore all the moves after they have been read.

        Returns:
            str: A formatted string containing the complete list of moves, or a
                message indicating that no moves were made if the queue is empty.
        """
        if self.moves.is_empty():
            return "No moves were made.\n"

        # Use a temporary queue to preserve and restore the original moves.
        temp_queue = Queue()  # Assumes your custom class is named Queue
        
        output_lines = ["Moves List:"]
        move_count = 0

        # 1. Process the original queue: read each item and save it to the temp queue.
        while not self.moves.is_empty():
            move = self.moves.dequeue()
            move_count += 1
            output_lines.append(f"  {move_count}: {move}")
            temp_queue.enqueue(move)

        # 2. Restore the original queue by moving all items back.
        while not temp_queue.is_empty():
            self.moves.enqueue(temp_queue.dequeue())
            
        return "\n".join(output_lines) + "\n"


    def verify_solution(self, display_moves=False):
        """
        Verifies the move count and returns a formatted report string.

        Args:
            display_moves (bool): If True, the formatted list of moves will
                                  be included in the returned report string.
        Returns:
            str: A multi-line string containing the verification report.
        """
        report_parts = []
    
        # Get the move count
        move_count = self.moves.size() 

        # Conditionally generate the moves string if the flag is set.
        if display_moves:
            report_parts.append(self._format_moves_string())

        expected_moves = 2**self.num_disks - 1

        report_parts.append(f"Total Moves: {move_count}")
        report_parts.append(f"Expected Moves: {expected_moves}")

        if move_count == expected_moves:
            report_parts.append("Result: SUCCESS\n")
        else:
            report_parts.append("Result: FAILED\n")
        
        return "\n".join(report_parts)

    
    def solve_iterative(self):
        """
        Solves the towers of hanoi problem for a game using num_disks.

        This methods solves the puzzle using a two-move iterative algorithm.

        Return:
            Queue (string): A queue of strings, where each string describes a single move.  
        """
        while self.target.size() < self.num_disks: # Loop ends once all disks are on target peg
            if self.move_number % 2 == 1:
                # Odd move: Move the smallest disk
                self._move_smallest_disk()
            else:
                # Even move: make the only other legal move
                self._make_other_legal_move()
        
            self.move_number += 1 # Increment the move counter
        
        # Return list of moves done
        return self.moves


    def _make_other_legal_move(self):
        """Makes the only legal move that doesn't involve the smallest disk.

        This helper identifies the two pegs not holding disk 1 and executes
        the only valid move between them (i.e., placing a smaller disk onto a
        larger one or onto an empty peg).

        Returns:
            None
        """
        
        # 1. Identify the two poles without the smallest disk
        match self.smallest_disk_location:
            case "source":
                # Smallest disk is on A, so the other pegs are B and C
                peg1, peg2 = self.aux, self.target
                peg1_name, peg2_name = "B", "C"
            case "aux":
                # Smallest disk is on B, so the other pegs are A and C
                peg1, peg2 = self.source, self.target
                peg1_name, peg2_name = "A", "C"
            case "target":
                # Smallest disk is on C, so the other pegs are A and B
                peg1, peg2 = self.source, self.aux
                peg1_name, peg2_name = "A", "B"
                
        # 2. Look at the top disk on those two poles
        peg1_disk = peg1.peek()
        peg2_disk = peg2.peek()

        # 3. Decide and execute the move
        # We move from peg 2 to peg 1 if peg1 is empty OR peg 2's disk is smaller.
        if peg1_disk is None or (peg2_disk is not None and peg2_disk < peg1_disk):
            # Move from peg2 to peg1
            disk = peg2.pop()
            peg1.push(disk)
            move_description = f"Move disk {disk} from tower {peg2_name} to tower {peg1_name}"
        
        # We move from peg 1 to peg 2 if peg 2 is empty OR peg 1's disk is smaller
        else:
            # Move from peg1 to peg2
            disk = peg1.pop()
            peg2.push(disk)
            move_description = f"Move disk {disk} from tower {peg1_name} to tower {peg2_name}"
            
        # 4. Record the move
        self.moves.enqueue(move_description)


    def _move_smallest_disk(self):
        """
        Dispatcher method for moving the smallest disk.

        This method checks if the total number of disks is odd or even
        and calls the corresponding helper function to perform the move
        according to the correct cyclical path.

        Returns:
            None
        """
        if self.num_disks % 2 == 1:
            # n is odd, use the odd path
            self._move_smallest_disk_odd_path()
        else:
            # n is even, use the even path
            self._move_smallest_disk_even_path()


    def _move_smallest_disk_even_path(self):
        """Determines the next move for the smallest disk for an even number of disks.

        When the total number of disks is even, the smallest disk (disk 1) moves
        in a predictable 'counter-clockwise' cycle: from A to C, then to B, then
        back to A. This method implements one step of that cycle.

        Returns:
            None
        """
        
        # 1. Determine the source and destination based on current location
        match self.smallest_disk_location:
            case "source":
                # If the smallest disk is on A, its next move is to B.
                source_peg = self.source
                dest_peg =   self.aux
                source_name, dest_name = "A", "B"
                self.smallest_disk_location = "aux"
            case "aux":
                # If the smallest disk is on B, its next move is to C.
                source_peg = self.aux
                dest_peg = self.target
                source_name, dest_name = "B", "C"
                self.smallest_disk_location = "target"
            case "target":
                # If the smallest disk is on C, its next move is back to A, completing the cycle.
                source_peg = self.target
                dest_peg = self.source
                source_name, dest_name = "C", "A"
                self.smallest_disk_location = "source"

        # 2. Get disk from source peg and move to destination peg
        disk = source_peg.pop()
        dest_peg.push(disk)
        
        # 3. Create move description and add it to the queue
        move_description = f"Move disk {disk} from tower {source_name} to tower {dest_name}."
        self.moves.enqueue(move_description)
        
    
    def _move_smallest_disk_odd_path(self):
        """Determines the next move for the smallest disk for an odd number of disks.

        When the total number of disks is odd, the smallest disk (disk 1) moves
        in a predictable 'clockwise' cycle: from A to B, then to C, and then
        back to A. This method implements one step of that cycle.

        Returns:
            None
        """
        
        # 1. Determine the source and destination based on current location
        match self.smallest_disk_location:
            case "source":
                # If the smallest disk is on A, its next move is to C.
                source_peg, dest_peg = self.source, self.target
                source_name, dest_name = "A", "C"
                self.smallest_disk_location = "target"  # Update location for the next turn
            case "target":
                # If the smallest disk is on C, its next move is to B.
                source_peg, dest_peg = self.target, self.aux
                source_name, dest_name = "C", "B"
                self.smallest_disk_location = "aux"
            case "aux":
                # If the smallest disk is on B, it moves back to A, completing the cycle.
                source_peg, dest_peg = self.aux, self.source
                source_name, dest_name = "B", "A"
                self.smallest_disk_location = "source"

        # 2. Get disk from source peg and move to destination peg
        disk = source_peg.pop()
        dest_peg.push(disk)
        
        # 3. Create the description and add it to the queue
        move_description = f"Move disk {disk} from tower {source_name} to tower {dest_name}."
        self.moves.enqueue(move_description)


    def solve_recursive(self):
        """
        Solves the Towers of Hanoi puzzle using a recursive algorithm.

        This method calls recursive helper function,
        and returns the completed queue of moves.

        Returns:
            Queue: A queue of strings describing each move.
        """
        
        # Start the process with all disks, the actual stack objects, and their names.
        self._recursive_helper(self.num_disks, self.source, self.target, self.aux, "A", "C", "B")
        
        return self.moves
    

    def _recursive_helper(self, disks_to_move, source_peg, target_peg, aux_peg, source_name, target_name, aux_name):
        """Recursively moves a tower of n disks from a source to a destination peg.

        This function implements the recursive solution for the Towers of
        Hanoi puzzle. It breaks the problem down into three steps:
        1. Move n-1 disks from the source to the auxiliary peg.
        2. Move the nth disk from the source to the destination peg.
        3. Move the n-1 disks from the auxiliary to the destination peg.

        Args:
            n (int): The number of disks to move in the current sub-problem.
            source (str): The name of the source peg (e.g., 'A').
            destination (str): The name of the destination peg (e.g., 'C').
            auxiliary (str): The name of the auxiliary/helper peg (e.g., 'B').

        Returns:
            None
        """

        # Base case: If there's only one disk, move it directly to the target.
        if disks_to_move == 1:
            disk = source_peg.pop()
            target_peg.push(disk)
            
            move_description = f"Move disk {disk} from tower {source_name} to tower {target_name}."
            self.moves.enqueue(move_description)
            return

        # 1. Recursively move n-1 disks from the source peg to the auxiliary peg,
        #    using the target peg as the temporary helper.
        self._recursive_helper(disks_to_move - 1, source_peg, aux_peg, target_peg, source_name, aux_name, target_name)

        # 2. Move the largest remaining disk (the nth disk) from the source peg
        #    to its final destination on the target peg.
        disk = source_peg.pop()
        target_peg.push(disk)

        move_description = f"Move disk {disk} from tower {source_name} to tower {target_name}"
        self.moves.enqueue(move_description)

        # 3. Recursively move the n-1 disks from the auxiliary peg to the target peg,
        #    now using the original source peg as the temporary helper.
        self._recursive_helper(disks_to_move - 1, aux_peg, target_peg, source_peg, aux_name, target_name, source_name)
