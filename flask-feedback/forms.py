from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Email
from flask_wtf import FlaskForm

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()], render_kw={"placeholder": "Enter Username"})
    password = PasswordField('Password', validators=[InputRequired()], render_kw={"placeholder": "Enter Password"})
    email = StringField('Email', validators=[InputRequired(), Email()], render_kw={"placeholder": "Enter Email"})
    first_name = StringField('First Name', validators=[InputRequired()], render_kw={"placeholder": "Enter First Name"})
    last_name = StringField('Last Name', validators=[InputRequired()], render_kw={"placeholder": "Enter Last Name"})
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()], render_kw={"placeholder": "Enter Username"})
    password = PasswordField('Password', validators=[InputRequired()], render_kw={"placeholder": "Enter Password"})
    submit = SubmitField('Login')

class DeleteForm(FlaskForm):
    submit = SubmitField('Delete')

class FeedbackForm(FlaskForm):
    title = StringField('Title', validators=[InputRequired()], render_kw={"placeholder": "Enter Title"})
    content = StringField('Content', validators=[InputRequired()], render_kw={"placeholder": "Enter Content"})
    submit = SubmitField('Submit')
