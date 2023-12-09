"""Message views test."""

# run these tests like:
# python -m unittest test_message_views.py

import os
from unittest import TestCase
from datetime import datetime

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app
from models import db, Message, User

# Don't have WTForms use CSRF at all, since it's a pain to test
app.config['WTF_CSRF_ENABLED'] = False

class LoginViewTestCase(TestCase):
    """Test views for login."""

    def setUp(self):
        """Create test client, add sample data."""
        self.client = app.test_client()

        # Set up the application context and create the database tables
        with app.app_context():
            db.drop_all()
            db.create_all()

            # Seed initial users
            testuser1 = User.signup(username="testuser1",
                                    email="test@test.com",
                                    password="testuser",
                                    image_url=None,
                                    header_image_url=None,
                                    bio=None
            )

            testuser2 = User.signup(username="testuser2", 
                                    email="test2@test.com",
                                    password="testuser2",
                                    image_url=None,
                                    header_image_url=None,
                                    bio=None
            )

            db.session.add(testuser1)
            db.session.add(testuser2)
            db.session.commit()

            # Seed initial messages 
            message_1 = Message(text="Test Message 1",
                                timestamp=datetime.utcnow(),
                                user_id=testuser1.id)
            message_2 = Message(text="Test Message 2",
                                timestamp=datetime.utcnow(),
                                user_id=testuser2.id)
            message_3 = Message(text="Test Message 3",
                                timestamp=datetime.utcnow(),
                                user_id=testuser2.id)
            for msg in [message_1, message_2, message_3]:
                db.session.add(msg)
            db.session.commit()

    def tearDown(self):
        """Tear down any data after each test."""

        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_signup_form(self):
        """Can a new user see the sign up form?"""

        with self.client as c:
            resp = c.get("/signup")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Username", html)
            self.assertIn("E-mail", html)
            self.assertIn("Password", html)
            self.assertIn("Image URL", html)
            self.assertIn("Header Image URL", html)
            self.assertIn("Bio", html)

    def test_signup_user(self):
        """Can a new user sign up?"""

        with self.client as c:
            resp = c.post("/signup", data={
                "username": "testuser3",
                "password": "password",
                "email": "testuser3@test.com",
                "image_url": "test_image.png",
                "header_image_url": "test_header_image.png",
                "bio": "test bio"
            }, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("testuser3", html)
            self.assertIn("test_image.png", html)
            self.assertIn("test_header_image.png", html)
