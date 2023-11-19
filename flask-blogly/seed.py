from models import User, db
from app import app

# Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()

    # If table isn't empty, empty it
    User.query.delete()

    # Add users
    shayne = User(first_name='Shayne', last_name="Coats", image_url="https://example.com/image1.jpg")
    rick = User(first_name='Rick', last_name="Astley", image_url="https://example.com/image2.jpg")

    # Add new objects to session, so they'll persist
    db.session.add(shayne)
    db.session.add(rick)

    # Commit--otherwise, this never gets saved!
    db.session.commit()