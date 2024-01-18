from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(db.Model):
    """User Model"""

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(80), unique=True, nullable=False)
    image_url = db.Column(db.Text)
    budgets = db.relationship('Budget', back_populates='user')
    saving = relationship("Saving", back_populates="user")

    @property
    def is_authenticated(self):
        """checks for authentication before request, see ref. app.py line 25"""
        return True

    @classmethod
    def signup(cls, username, password, email, image_url):
        """Sign up user. Hashes password and adds user to the system."""

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')
        user = cls(username=username, password=hashed_pwd, email=email, image_url=image_url)
        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`"""

        user = cls.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        return False

class Budget(db.Model):
    """Budget Model"""

    __tablename__ = "budget"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.Date)
    user = db.relationship('User', back_populates='budgets')
    income = relationship("Income", back_populates="budget", cascade="all, delete-orphan")
    expense = relationship("Expense", back_populates="budget", cascade="all, delete-orphan")
    

class Income(db.Model):
    """Income Model"""

    __tablename__ = "income"

    id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'))
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, default=0)
    budget = relationship("Budget", back_populates="income")

class Expense(db.Model):
    """Expense Model"""

    __tablename__ = "expense"

    id = db.Column(db.Integer, primary_key=True)
    budget_id = db.Column(db.Integer, db.ForeignKey('budget.id'))
    category = db.Column(db.String(50), nullable=False)
    amount = db.Column(db.Float, default=0)
    budget = relationship("Budget", back_populates="expense")


class Saving(db.Model):
    """Savings goals Model"""

    __tablename__ = 'saving'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    name = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    user = relationship("User", back_populates="saving")

def connect_db(app):
    """Connect this database to the provided Flask app."""

    db.app = app
    db.init_app(app)