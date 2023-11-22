# Import necessary modules
from flask import Flask, render_template, redirect, flash, session
from models import db, connect_db, Pet
from forms import AddPetForm, EditPetForm

# Create Flask app instance
app = Flask(__name__)

# Configure app settings
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "secret"

# Connect to the database
connect_db(app)

# Define home route
@app.route('/')
def home():
    """Show homepage with list of pets"""
    pets = Pet.query.all()
    return render_template('home.html', pets=pets)

# Define add pet route
@app.route('/add', methods=["GET", "POST"])
def add_pet():
    """Show add pet form and handle form submission"""
    form = AddPetForm()
    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        available = form.available.data  
        pet = Pet(name=name, species=species, photo_url=photo_url, age=age, notes=notes, available=available)
        db.session.add(pet)
        db.session.commit()
        flash('Pet successfully added', 'success')
        return redirect('/')
    else:
        # Handle form validation errors
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'{field}: {error}', 'error')
        return render_template('add_pet.html', form=form)

# Define pet details route
@app.route('/<int:pet_id>', methods=["GET", "POST"])
def pet_details(pet_id):
    """Show pet details and handle edit form submission"""
    pet = Pet.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)
    if form.validate_on_submit():
        form.populate_obj(pet)
        db.session.commit()
        flash('Pet successfully edited', 'success')
        return redirect('/')
    return render_template('pet_details.html', pet=pet, form=form)