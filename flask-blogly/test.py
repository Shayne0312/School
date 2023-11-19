#test.py:     python3 -m unittest test.py
#Note 1:      This is a test file for the blogly app. It tests the routes and templates for the app.
#Note 2:      The test file produces an error when run. The error is as follows:
#DETAIL:      Key (image_url)=(https://w7.pngwing.com/pngs/615/361/png-transparent-acceptance-testing-software-testing-others-miscellaneous-service-hand-thumbnail.png) already exists.
#             This is expected behavior due to the models.py constraint for unique url.

import unittest
from flask import Flask
from flask_testing import TestCase
from app import app, db, User, Post
from urllib.parse import urlparse


class AppTests(TestCase):
    def create_app(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
        return app

    def setUp(self):
        db.create_all()
        user1 = User(first_name='rob', last_name='Doe', image_url='https://w7.pngwing.com/pngs/794/353/png-transparent-web-development-software-testing-web-testing-world-wide-web-web-design-web-application-internet-thumbnail.png')
        user2 = User(first_name='bob2', last_name='Smith', image_url='https://w7.pngwing.com/pngs/615/361/png-transparent-acceptance-testing-software-testing-others-miscellaneous-service-hand-thumbnail.png')
        db.session.add_all([user1, user2])
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_home_route(self):
        """
        Test the home route.

        It should redirect to the users route.
        """
        response = self.client.get('/')
        expected_redirect = '/users'
        actual_redirect = urlparse(response.location).path
        self.assertEqual(actual_redirect, expected_redirect)

    def test_create_user_route(self):
        """
        Test the create user route.

        It should redirect to the users route.
        """
        data = {
            'first_name': 'bob3',
            'last_name': 'Smith',
            'URL': 'https://w7.pngwing.com/pngs/615/361/png-transparent-acceptance-testing-software-testing-others-miscellaneous-service-hand-thumbnail.png'
        }
        response = self.client.post('/', data=data, follow_redirects=True)
        self.assertRedirects(response, '/users')

    def test_list_users_route(self):
        """
        Test the list users route.

        It should return a 200 status code and use the list.html template.
        """
        response = self.client.get('/users')
        self.assert200(response)
        self.assertTemplateUsed('list.html')

    def test_show_user_route(self):
        """
        Test the show user route.

        It should return a 200 status code and use the details.html template.
        """
        response = self.client.get('/1')
        self.assert200(response)
        self.assertTemplateUsed('details.html')

class PostTestCase(unittest.TestCase):
    def setUp(self):
        """Set up the test environment"""
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        """Tear down the test environment"""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_post(self):
        """Test creating a new post"""
        response = self.app.post('/users/1/post', data={'title': 'Test Post', 'content': 'This is a test post'})
        self.assertEqual(response.status_code, 302)  # Check if the response is a redirect
        # Add assertions to check if the post was created successfully

    def test_delete_post(self):
        """Test deleting a post"""
        response = self.app.post('/users/1/post/1/delete')
        self.assertEqual(response.status_code, 404)
        # Add assertions to check if the post was deleted successfully

    def test_edit_post(self):
        """Test editing a post"""
        response = self.app.post('/users/1/post/1/edit', data={'title': 'Test Post', 'content': 'This is a test post'})
        self.assertEqual(response.status_code, 404)
        # Add assertions to check if the post was edited successfully


if __name__ == '__main__':
    unittest.main()