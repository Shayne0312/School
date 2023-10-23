from wordfinder import WordFinder
import unittest
import tracemalloc

class TestWordFinder(unittest.TestCase):
    def test_parse(self):
        wf = WordFinder('words.txt')
        self.assertIn('Aaronite', wf.words) 
    
    def test_random(self):
        wf = WordFinder('words.txt')
        word = wf.random()
        self.assertIn(word, wf.words)

if __name__ == '__main__':
    tracemalloc.start()
    unittest.main()
    
    snapshot = tracemalloc.take_snapshot()
    top_stats = snapshot.statistics('lineno')
    for stat in top_stats:
        print(stat)

# Usage:
# open terminal
# navigate to directory where file is located
# python3 test_wordfinder.py

# Added tracemalloc to test memory usage
# Added tracemalloc.start() to start tracing memory allocations
# Added snapshot = tracemalloc.take_snapshot() to take snapshot of memory allocations
# Added top_stats = snapshot.statistics('lineno') to get statistics of memory allocations

# Using tracealloc:
# I found that the parse method was using the most memory because it was
# creating a list of all the words in the words.txt file
# This was for learning purposes only.