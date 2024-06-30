import os

def load_ascii_art():
    with open(os.path.join(os.path.dirname(__file__), 'ascii_art.txt'), 'r') as f:
        lines = f.readlines()
        # Print the ASCII art
        for line in lines:
            # Remove the newline character
            # before printing the line
            # but keep the indentation
            # of the original text
            print(line.strip('\n'))
