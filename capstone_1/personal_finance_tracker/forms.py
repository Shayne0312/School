from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, DecimalField
from wtforms.validators import DataRequired, Email, Length


class SignupForm(FlaskForm):
    """Signup form."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
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


class BudgetForm(FlaskForm):
    date = DateField('Budget Date', format='%Y-%m-%d', validators=[DataRequired()])
    income_category = StringField('Income Category', validators=[DataRequired()])
    income_amount = DecimalField('Income Amount', validators=[DataRequired()])
    expense_category = StringField('Expense Category', validators=[DataRequired()])
    expense_amount = DecimalField('Expense Amount', validators=[DataRequired()])
