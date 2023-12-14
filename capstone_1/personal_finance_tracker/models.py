"""SQLAlchemy models for Dream Financial"""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """User Model"""

    __tablename__ = 'user'

    id = db.Column(
        db.Integer, 
        primary_key=True
    )

    username = db.Column(
    db.String(80), 
    unique=True, 
    nullable=False
    )

    password = db.Column(
    db.String(128), 
    nullable=False
    )

    email = db.Column(
        db.String(80), 
        unique=True, 
        nullable=False
    )

    image_url = db.Column(
        db.Text
    )

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

    @property
    def is_authenticated(self):
        return True

    @classmethod
    def signup(cls, username, password, email, image_url):
        """Sign up user.
        Hashes password and adds user to system.
        """
        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            password=hashed_pwd,
            email=email,
            image_url=image_url,
        )

        db.session.add(user)
        return user
    
    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`"""

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user
        return False

    
def connect_db(app):
    """Connect this database to provided Flask app."""

    db.app = app
    db.init_app(app)