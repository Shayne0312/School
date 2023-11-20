from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

def connect_db(app):
    # Connect the database to the Flask app
    db.app = app
    db.init_app(app)

# ************************************USER**************************************

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

# ************************************POST**************************************

post_tags = db.Table(
    'post_tags',
    db.Column('post_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'), primary_key=True)
)

class Post(db.Model):
    # Define the Post model
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(50), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='posts')
    tags = db.relationship('Tag', secondary=post_tags, backref='post')

    @classmethod
    def get_by_id(cls, id):
        # Retrieve a post by its ID
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_user_id(cls, user_id):
        # Retrieve all posts for a given user
        return cls.query.filter_by(user_id=user_id).all()

    @classmethod
    def get_all(cls):
        # Retrieve all posts
        return cls.query.all()

    def __repr__(self):
        # Define a string representation of the Post object
        return f"<Post id={self.id} title={self.title} content={self.content} created_at={self.created_at} user_id={self.user_id}>"

# ************************************TAG**************************************

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship('User', backref='tags')
    posts = db.relationship('Post', secondary=post_tags, backref='tag')

    @classmethod
    def get_by_id(cls, id):
        # Retrieve a tag by its ID
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_name(cls, name):
        # Retrieve a tag by its name
        return cls.query.filter_by(name=name).first()

    @classmethod
    def get_all(cls):
        # Retrieve all tags
        return cls.query.all()

    def __repr__(self):
        # Define a string representation of the Tag object
        return f"<Tag id={self.id} name={self.name}>"