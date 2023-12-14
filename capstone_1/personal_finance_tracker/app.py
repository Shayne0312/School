import os

from flask import Flask, render_template, request, flash, redirect, url_for, session, g
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, login_user

from forms import LoginForm, SignupForm, EditProfileForm
from models import db, connect_db, User
from functools import wraps

CURR_USER_KEY = "curr_user"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'postgresql:///finance')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "secretkey")

connect_db(app)

##############################################################################
# User signup/login/logout

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    
    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
        print("User is authenticated:", g.user.is_authenticated)
    else:
        g.user = None

def do_login(user):
    """Login user"""

    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

def redirect_if_missing(func):
    """Handles auth if not logged in."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        if not g.user:
            flash("Access unauthorized.", "danger")
            return redirect("/")
        return func(*args,**kwargs)
    return wrapper

##############################################################################
# Routes

@app.route('/')
def index():
    return render_template('homepage.html', user=g.user)


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup."""

    form = SignupForm()

    if form.is_submitted() and form.validate():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or "/static/images/default.jpg"
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)
        print("signed up successfully")
        return redirect("/")
    else:
        return render_template('users/signup.html', form=form)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()
    if form.is_submitted():
        user = User.authenticate(
            form.username.data,
            form.password.data
        )
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")
        flash("Invalid credentials.", 'danger')
    return render_template('users/login.html', form=form)

@app.route('/logout')
def logout():
    """Handles user logout"""
    do_logout()
    flash("You have successfully logged out", "success")
    return redirect(url_for('login'))

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data 
        # update other fields
        db.session.commit()
        flash('Profile Updated')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        # populate other fields
    return render_template('edit_profile.html', form=form)

@app.route('/reauthorize', methods=['GET', 'POST'])
def reauthorize():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(
            form.username.data,
            form.password.data
        )
        if user:
            login_user(user)
            return redirect(url_for('edit_profile'))
        else:
            flash('Invalid login credentials', 'error')
    return render_template('reauthorize.html', form=form)

@app.route('/profile/<int:user_id>')
def profile(user_id):
    if not g.user:
        flash("Please sign in to view this page.", "error")
        return redirect(url_for('login'))

    if g.user.id == user_id:
        user = User.query.get_or_404(user_id)
        return render_template('users/profile.html', user_id=user_id, user=user)
    else:
        flash("You do not have permission to view this page.", "error")
        return redirect(url_for('index'))
    
@app.route('/budgeting', methods=["GET", "POST"])
def budgeting():
    if request.method == "POST":
        income = request.form['income']
        expenditure = request.form['expenditure']
        return render_template('budgeting.html', income=income, expenditure=expenditure)
    else:
        return render_template('budgeting.html')
    
@app.route('/investing')
def investing():
    
    return render_template('investing.html')

@app.route('/saving')
def saving():
    return render_template('saving.html')

if __name__ == '__main__':
    app.run(debug=True)