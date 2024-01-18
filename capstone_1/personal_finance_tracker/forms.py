from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, DateField, FieldList, FormField, IntegerField
from wtforms.validators import DataRequired, Email, Length, NumberRange


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
    image_url = StringField('(Optional) Image URL')
    username = StringField('(Optional) Username')
    password = PasswordField('Password')
    email = StringField('E-mail')

class IncomeEntryForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[DataRequired()])

class ExpenseEntryForm(FlaskForm):
    category = StringField('Category', validators=[DataRequired()])
    amount = IntegerField('Amount', validators=[NumberRange(min=0)])
    
class BudgetForm(FlaskForm):
    date = StringField('Date', validators=[DataRequired()])
    income_entries = FieldList(FormField(IncomeEntryForm), min_entries=1)
    expense_entries = FieldList(FormField(ExpenseEntryForm), min_entries=1)

class SavingForm(FlaskForm):
    goal_date = DateField('Target Date', validators=[DataRequired()])
    goal_name = StringField('Goal Name', validators=[DataRequired()])
    goal_amount = IntegerField('Amount ($)', validators=[DataRequired()])