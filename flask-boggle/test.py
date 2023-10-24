from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle


class FlaskTests(TestCase):
    def setUp(self):
        """Set up the test environment before each test."""
        self.client = app.test_client()
        app.config['TESTING'] = True

    def test_homepage(self):
        """Test if information is in the session and HTML is displayed correctly."""
        with self.client:
            response = self.client.get('/')
            self.assertIn('board', session)  # File to test: app.py
            self.assertIsNone(session.get('highscore'))  # File to test: app.py
            self.assertIsNone(session.get('nplays'))  # File to test: app.py
            self.assertIn(b'<p>High Score:', response.data)  # File to test: index.html
            self.assertIn(b'Score:', response.data)  # File to test: index.html
            self.assertIn(b'Seconds Left:', response.data)  # File to test: index.html

    def test_word_validity(self):
        """Test if a word is valid on the board and in the dictionary."""
        with self.client as client:
            with client.session_transaction() as sess:
                sess['board'] = [
                    ["C", "A", "T", "T", "T"],
                    ["C", "A", "T", "T", "T"],
                    ["C", "A", "T", "T", "T"],
                    ["C", "A", "T", "T", "T"],
                    ["C", "A", "T", "T", "T"]
                ]
        response = self.client.get('/check-word?word=cat')  # File to test: app.py
        self.assertEqual(response.json['result'], 'ok')

    def test_word_not_on_board(self):
        """Test if a word is not on the board."""
        self.client.get('/')
        response = self.client.get('/check-word?word=impossible')  # File to test: app.py
        self.assertEqual(response.json['result'], 'not-on-board')

    def test_non_english_word(self):
        """Test if a non-English word is not in the dictionary."""
        self.client.get('/')
        response = self.client.get('/check-word?word=fsjdakfkldsfjdslkfjdlksf')  # File to test: app.py
        self.assertEqual(response.json['result'], 'not-word')