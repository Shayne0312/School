from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Optional, URL, NumberRange, AnyOf

class AddPetForm(FlaskForm):
    """Form for adding pets"""
    name = StringField("Pet Name", validators=[InputRequired()], render_kw={"placeholder": "Enter pet name"})
    species = SelectField("Species", choices=[('cat', 'Cat'), ('dog', 'Dog'), ('porcupine', 'Porcupine')], validators=[InputRequired(message='Please select a species.')])
    photo_url = StringField("Photo URL", validators=[Optional(), URL(message='Invalid URL')], render_kw={"placeholder": "Enter JPG/PNG URL"})
    age = IntegerField("Age", validators=[Optional(), NumberRange(min=0, max=30)], render_kw={"placeholder": "1 - 30"})
    notes = TextAreaField("Notes", validators=[Optional()], render_kw={"placeholder": "Vaccinations, feeding schedule, etc."})
    available = BooleanField("Available")

class EditPetForm(FlaskForm):
    """Form for editing pets"""
    photo_url = StringField("Photo URL", validators=[Optional(), URL()])
    notes = TextAreaField("Notes", validators=[Optional()])
    available = BooleanField("Available")