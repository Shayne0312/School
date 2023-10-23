"""Word Finder: finds random words from a dictionary."""
import random

class WordFinder:
    def __init__(self, path):  
        """Read dictionary and reports # items read."""
        with open(path, 'r', encoding='cp1252') as dict_file:
            self.words = self.parse(dict_file)
        print(f"{len(self.words)} words read")

    def parse(self, dict_file):
        """Parse dict_file -> list of words."""
        return [w.strip() for w in dict_file]

    def random(self):
        """Return random word."""
        return random.choice(self.words)
    
wf = WordFinder('words.txt')
print(wf.random())

# Usage:
# Open terminal
# Navigate to the directory where the file is located
# python3 wordfinder.py

# added with statement to fix unclosed file error(words.txt)
# the words.txt file automatically

# added encoding to fix UnicodeDecodeError
# The line with open(path, 'r', encoding='cp1252') as dict_file:
# was added to fix the UnicodeDecodeError: 'charmap' codec can't
# decode byte 0x9d in position 1023: character maps to <undefined> error