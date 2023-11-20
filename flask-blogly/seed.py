from models import User, db
from app import app

# Create all tables
with app.app_context():
    db.drop_all()
    db.create_all()

    # If table isn't empty, empty it
    User.query.delete()

    # Add users
    bilbo = User(first_name='Bilbo', last_name="Baggins", image_url="https://upload.wikimedia.org/wikipedia/en/7/78/Bilbo_Baggins.jpg")
    gandaulf = User(first_name='Gandaulf', last_name="Grey", image_url="https://cdn.costumewall.com/wp-content/uploads/2017/01/gandalf-the-grey.jpg")
    ariel = User(first_name='Ariel', last_name="Daddysgirl", image_url="https://www.gardeningknowhow.com/wp-content/uploads/2019/09/flower-color.jpg")
    
    # Add new objects to session, so they'll persist
    db.session.add(bilbo)
    db.session.add(gandaulf)
    db.session.add(ariel)

    # Commit--otherwise, this never gets saved!
    db.session.commit()