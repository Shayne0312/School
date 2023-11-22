from models import db, Pet
from app import app

# Create the database tables
with app.app_context():
    db.drop_all()
    db.create_all()

    # Create sample pet objects
    doge = Pet(name="Doge", species="dog", photo_url="https://pngimg.com/uploads/doge_meme/doge_meme_PNG22.png")
    nyan = Pet(name="Nyan", species="cat", photo_url="https://www.pngall.com/wp-content/uploads/2016/06/Nyan-Cat-Free-Download-PNG.png")
    bob = Pet(name="Bob", species="porcupine", photo_url="https://www.pngitem.com/pimgs/m/31-312164_porcupine-png-transparent-png.png")

    # Add the pets to the session and commit changes to the database
    db.session.add(doge)
    db.session.add(nyan)
    db.session.commit()