from models import User, Feedback, bcrypt
from app import app, db

# Create database tables
with app.app_context():
    db.drop_all()
    db.create_all()

    # Seed the database
    users = [
        User(username='admin', password=bcrypt.generate_password_hash('password').decode('utf-8'), email='admin@example.com', first_name='Bill', last_name='Murray'),
        User(username='user1', password=bcrypt.generate_password_hash('password1').decode('utf-8'), email='user1@example.com', first_name='Ben', last_name='Dover'),
        User(username='user2', password=bcrypt.generate_password_hash('password2').decode('utf-8'), email='user2@example.com', first_name='Hacky', last_name='Sack'),
    ]
    for user in users:
        db.session.add(user)
    db.session.commit()

    # Seed the feedback table
    feedbacks = [
        Feedback(title='Feedback 1', content='This is feedback 1.', username='admin'),
        Feedback(title='Feedback 2', content='This is feedback 2.', username='user1'),
        Feedback(title='Feedback 3', content='This is feedback 3.', username='user2'),
    ]
    for feedback in feedbacks:
        db.session.add(feedback)
    db.session.commit()

    # Close database connection
    db.session.close()