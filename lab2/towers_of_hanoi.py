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

         # Load disks onto the source peg from largest to smallest
        for i in range(self.num_disks, 0, -1):
            self.source.push(i)

    
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
        """Makes the only legal move between the two pegs not holding the smallest disk."""
        
        # 1. Identify the two poles without the smallest disk
        match self.smallest_disk_location:
            case "source":
                peg1, peg2 = self.aux, self.target
                peg1_name, peg2_name = "B", "C"
            case "aux":
                peg1, peg2 = self.source, self.target
                peg1_name, peg2_name = "A", "C"
            case "target":
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
        """
        if self.num_disks % 2 == 1:
            # n is odd, use the odd path
            self._move_smallest_disk_odd_path()
        else:
            # n is even, use the even path
            self._move_smallest_disk_even_path()

    def _move_smallest_disk_even_path(self):
        """Handles the movement of disk 1 for an even number of total disks."""
        
        # 1. Determine the source and destination based on current location
        match self.smallest_disk_location:
            case "source":
                source_peg = self.source
                dest_peg =  self.aux
                source_name, dest_name = "A", "B"
                self.smallest_disk_location = "aux"  # Update for the next turn
            case "aux":
                source_peg = self.aux
                dest_peg = self.target
                source_name, dest_name = "B", "C"
                self.smallest_disk_location = "target"
            case "target":
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
        """Handles the movement of disk 1 for an odd number of total disks."""
        
        # 1. Determine the source and destination based on current location
        match self.smallest_disk_location:
            case "source":
                # Move from Source to Target
                source_peg, dest_peg = self.source, self.target
                source_name, dest_name = "A", "C"
                self.smallest_disk_location = "target"  # Update for the next turn
            case "target":
                # Move from Target to Auxiliary
                source_peg, dest_peg = self.target, self.aux
                source_name, dest_name = "C", "B"
                self.smallest_disk_location = "aux"
            case "aux":
                # Move from Auxiliary to Source
                source_peg, dest_peg = self.aux, self.source
                source_name, dest_name = "B", "A"
                self.smallest_disk_location = "source"

        # 2. Get disk from source peg and move to destination peg
        disk = source_peg.pop()
        dest_peg.push(disk)
        
        # 3. Create the description and add it to the queue
        move_description = f"Move disk {disk} from tower {source_name} to tower {dest_name}."
        self.moves.enqueue(move_description)