import unittest
from flask import Flask
import app

# python test.py

class YourAppTestCase(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()
        
    def test_currency_conversion(self):
        result = app.get_currency_conversion('USD', 'EUR', 100)
        self.assertIsNotNone(result, "Expected result is not None")
        self.assertIsInstance(result, float, "Expected result is float")

if __name__ == '__main__':
    unittest.main()

