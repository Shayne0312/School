"""Message model tests."""

# run these tests like:
#python -m unittest test_message_model.py


import os
from unittest import TestCase
from datetime import datetime

os.environ['DATABASE_URL'] = "postgresql:///warbler-test"

from app import app
from models import db, User, Message, Follows, Likes



class MessageModelTestCase(TestCase):
    """Test views for messages."""

    def setUp(self):
        """Create test client, add sample data."""

        self.client = app.test_client()

        with app.app_context():
            db.drop_all()
            db.create_all()

            # Seed initial users
            testuser1 = User.signup(
                username="testuser1",
                email="test@test.com",
                password="testuser",
                image_url=None,
                header_image_url=None,
                bio=None
            )

            testuser2 = User.signup(
                username="testuser2", 
                email="test2@test.com",
                password="testuser2",
                image_url=None,
                header_image_url=None,
                bio=None
                )
            
            db.session.add(testuser1)
            db.session.add(testuser2)
            db.session.commit()

            all_follows = Follows.query.all()
            for test_follow in all_follows:
                db.session.delete(test_follow)
            db.session.commit()

            all_messages = Message.query.all()
            for test_message in all_messages:
                db.session.delete(test_message)
            db.session.commit()

            all_likes = Likes.query.all()
            for test_like in all_likes:
                db.session.delete(test_like)
            db.session.commit()

            all_users = User.query.all()
            for test_user in all_users:
                db.session.delete(test_user)
            db.session.commit()

            user1 = User(
                username="testuser",
                email="testemail@test.com",
                password="HASHED_PASSWORD"
            )

            db.session.add(user1)
            db.session.commit()

            self.client = app.test_client()
    
    def tearDown(self):
        """Tear down any data after each test."""

        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_message_model(self):
        """Does basic model work?"""

        with app.app_context():
            user1 = User.query.first()
            m = Message(
                text="Test Message",
                timestamp=datetime.utcnow(),
                user_id=user1.id
            )
    
            db.session.add(m)
            db.session.commit()
    
            # User data is stored in the database
            self.assertEqual(m.text,"Test Message")
            self.assertIsNotNone(m.timestamp)
            self.assertIsNotNone(m.id)
            self.assertEqual(m.user_id,user1.id)
    
            # User should have a user relationship
            self.assertEqual(m.user, user1)

    def test_missing_required_data(self):
        """ Does model throw error with missing required data """

        with app.app_context():
            user1 = User.query.first()
            messages = [
                Message(text="Test Message",timestamp=datetime.utcnow()),
                Message(timestamp=datetime.utcnow(),user_id=user1.id),
                ]

            for m in messages:
                db.session.rollback()
                try:
                    print('message: ',m)
                    db.session.add(m)
                    db.session.commit()
                    exception = None
                except Exception:
                    exception = "Error"
                # User data is not stored in the database
                self.assertEqual(exception,"Error")
    
    def test_missing_data_with_defaults(self):
        """ Does model populate default with missing data that has defaults """
        
        with app.app_context():
            user1 = User.query.first()
            messages = [Message(text="Test Message",user_id=user1.id)]

            for m in messages:
                db.session.rollback()
                try:
                    print('message: ',m)
                    db.session.add(m)
                    db.session.commit()
                    exception = None
                except Exception:
                    exception = "Error"
                # User data is not stored in the database
                self.assertIsNone(exception)
        