from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    """Signup form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(),Length(min=6)])
    email = StringField('E-mail', validators=[Email()])
    image_url = StringField('(Optional) Image URL')

class LoginForm(FlaskForm):
    """Login form."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])

class EditProfileForm(FlaskForm):
    """Form for editing user information."""

    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[Length(min=6)])
    email = StringField('E-mail', validators=[Email()])
    image_url = StringField('(Optional) Image URL')
