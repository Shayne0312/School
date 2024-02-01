"""Seed Database"""

from models import User, bcrypt
from app import app, db

# Seed database
with app.app_context():
    # Drop and recreate tables
    db.drop_all()
    db.create_all()

    # Create initial users
    users_data = [
        {'username': 'admin', 'password': 'password', 'email': 'admin@example.com', 'image_url': '/static/images/default.jpg'},
        {'username': 'user1', 'password': 'password1', 'email': 'user1@example.com', 'image_url': '/static/images/default.jpg'},
        {'username': 'user2', 'password': 'password2', 'email': 'user2@example.com', 'image_url': '/static/images/default.jpg'},
    ]

    for user_data in users_data:
        # Hash the password before creating the user
        user_data['password'] = bcrypt.generate_password_hash(user_data['password']).decode('utf-8')
        user = User(**user_data)
        db.session.add(user)

    # Commit changes to the database
    db.session.commit()

    # Close the session
    db.session.close()

    print('Database seeded!')