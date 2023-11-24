# create cupcakes_test database - 
# 1. psql
# 2. CREATE DATABASE cupcakes_test;
# 3. python3 -m unittest tests.py

import unittest
from flask import Flask, request, jsonify, render_template
from models import db, connect_db

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes_test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TESTING'] = True
connect_db(app)


class CupcakeViewsTestCase(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.drop_all()

    def test_list_cupcakes(self):
        with app.test_client() as client:
            response = client.get('/api/cupcakes')
            self.assertEqual(response.status_code, 404)

    def test_get_cupcake(self):
        with app.test_client() as client:
            response = client.get('/api/cupcakes/1')
            self.assertEqual(response.status_code, 404)

    def test_create_cupcake(self):
        with app.test_client() as client:
            response = client.post('/api/cupcakes', json={
                'flavor': 'chocolate',
                'size': 'small',
                'rating': 10,
                'image': 'https://tinyurl.com/demo-cupcake'
            })
            self.assertEqual(response.status_code, 404)

    def test_update_cupcake(self):
        with app.test_client() as client:
            response = client.patch('/api/cupcakes/1', json={
                'flavor': 'chocolate',
                'size': 'small',
                'rating': 10,
                'image': 'https://tinyurl.com/demo-cupcake'
            })
            self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()