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

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"
    
    user_savings_goals = relationship("SavingsGoal", back_populates="user")
    user_budgets = relationship("Budget", back_populates="user")

    @property
    def is_authenticated(self):
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
    income_category = db.Column(db.String(50), nullable=False)
    income_amount = db.Column(db.Integer, default=0)
    expense_category = db.Column(db.String(50), nullable=False)
    expense_amount = db.Column(db.Integer, default=0)

    def __repr__(self):
        return f"<Budget #{self.id}: {self.date} - Income: {self.income_category} - {self.income_amount}, Expenses: {self.expense_category} - {self.expense_amount}>"

    user = relationship("User", back_populates="user_budgets")


class SavingsGoal(db.Model):
    """Model for savings goals."""

    __tablename__ = 'savings_goals'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    target_date = db.Column(db.Date, nullable=False)

    # Define a relationship with the User model
    user = relationship("User", back_populates="user_savings_goals")

def connect_db(app):
    """Connect this database to the provided Flask app."""
    db.app = app
    db.init_app(app)
