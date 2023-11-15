from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    # Connect the database to the Flask app
    db.app = app
    db.init_app(app)

class User(db.Model):
    # Define the User model
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(50), nullable=False, unique=True)
    last_name = db.Column(db.String(50), nullable=False, unique=False)
    image_url = db.Column(db.String(1000), nullable=True, unique=True)

    @classmethod
    def get_by_id(cls, id):
        # Retrieve a user by their ID
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_name(cls, name):
        # Retrieve a user by their name
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_all(cls):
        # Retrieve all users
        return cls.query.all()

    def __repr__(self):
        # Define a string representation of the User object
        return f"<User id={self.id} first_name={self.first_name} last_name={self.last_name}>"