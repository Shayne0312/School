from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField
from wtforms.validators import InputRequired, Email, NumberRange, AnyOf

class LuckyNumberForm(FlaskForm):
    name = StringField('name', validators=[InputRequired()])
    email = StringField('email', validators=[InputRequired(), Email()])
    year = IntegerField('year', validators=[InputRequired(), NumberRange(min=1900, max=2000)])
    color = StringField('color', validators=[InputRequired(), AnyOf(['red', 'green', 'orange', 'blue'])])