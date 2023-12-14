"""Seed Database"""

from models import User, bcrypt
from app import app, db

# Seed database
with app.app_context():
    db.drop_all()
    db.create_all()

    # Create initial users
    users = [
        User(username='admin', password=bcrypt.generate_password_hash('password').decode('utf-8'), email='admin@example.com', image_url = '/static/images/default.jpg'),
        User(username='user1', password=bcrypt.generate_password_hash('password1').decode('utf-8'), email='user1@example.com', image_url = '/static/images/default.jpg'),
        User(username='user2', password=bcrypt.generate_password_hash('password2').decode('utf-8'), email='user2@example.com', image_url = '/static/images/default.jpg'),
    ]
    for user in users:
       db.session.add(user)
    db.session.commit()

    db.session.close()

    print('Database seeded!')