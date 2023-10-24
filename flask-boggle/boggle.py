from random import choice
import string

class Boggle:
    def __init__(self):
        self.words = self.read_dict("words.txt")

    def read_dict(self, dict_path):
        """Read and return all words in the dictionary."""
        with open(dict_path) as dict_file:
            words = [w.strip() for w in dict_file]
        return words

    def make_board(self):
        """Make and return a random Boggle board."""
        board = [[choice(string.ascii_uppercase) for _ in range(5)] for _ in range(5)]
        return board

    def check_valid_word(self, board, word):
        """Check if a word is a valid word in the dictionary and/or on the Boggle board."""
        word = word.lower()
        word_exists = word in self.words
        valid_word = self.find(board, word.upper())

        if word_exists and valid_word:
            return "ok"
        elif word_exists and not valid_word:
            return "not-on-board"
        else:
            return "not-word"

    def find_from(self, board, word, y, x, seen):
        """Recursively find if a word can be formed on the board, starting at (x, y)."""
        if x > 4 or y > 4:
            return False

        if board[y][x] != word[0]:
            return False

        if (y, x) in seen:
            return False

        if len(word) == 1:
            return True

        seen = seen | {(y, x)}

        for dy in [-1, 0, 1]:
            for dx in [-1, 0, 1]:
                if dy == 0 and dx == 0:
                    continue
                if self.find_from(board, word[1:], y + dy, x + dx, seen):
                    return True

        return False

    def find(self, board, word):
        """Check if a word can be found on the Boggle board."""
        for y in range(5):
            for x in range(5):
                if self.find_from(board, word, y, x, seen=set()):
                    return True

        return False