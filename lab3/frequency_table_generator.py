"""
A utility module to generate a frequency table from a text string.
"""
from collections import defaultdict

def generate_frequency_table(text: str) -> dict[str, int]:
    """
    Generates a frequency table from an input text string.

    This function:
    - Is case-sensitive

    Args:
        text (str): The input string to analyze.

    Returns:
        dict[str, int]: A dictionary mapping each character to its
                        frequency count (e.g., {'A': 22, 'B': 16}).
    """
    # Use defaultdict to automatically handle new keys with a 0 count
    frequencies = defaultdict(int)
    
    for char in text:
        frequencies[char.upper()] += 1
            
    return dict(frequencies)
