from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """
    Connect the database to the Flask app
    """
    db.app = app
    db.init_app(app)

class Pet(db.Model):
    """
    Pet Model
    """
    __tablename__ = "pets"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False)
    species = db.Column(db.Text, nullable=False)
    photo_url = db.Column(db.Text)
    age = db.Column(db.Integer)
    notes = db.Column(db.Text)
    available = db.Column(db.Boolean, nullable=False, default=True)

    def __repr__(self):
        """
        Return a string representation of the Pet object
        """
        return f"<Pet {self.id} {self.name} {self.species} {self.age} {self.available}>"