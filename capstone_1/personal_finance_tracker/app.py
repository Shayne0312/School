import os
from flask import Flask, render_template, request, flash, redirect, url_for, session, g, jsonify, abort
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
from datetime import datetime
from forms import LoginForm, SignupForm, EditProfileForm, BudgetForm, SavingForm, IncomeEntryForm, ExpenseEntryForm
from models import db, connect_db, User, Budget, Saving, Income, Expense
from functools import wraps

CURR_USER_KEY = "curr_user"
bcrypt = Bcrypt()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql:///finance')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', "supersecretcryptokey")

connect_db(app)

################################################## Helper Functions ##################################################
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    g.user = User.query.get(session.get(CURR_USER_KEY)) if CURR_USER_KEY in session else None

def do_login(user):
    """Login user"""
    session[CURR_USER_KEY] = user.id

def do_logout():
    """Logout user."""
    session.pop(CURR_USER_KEY, None)

def redirect_if_missing(func):
    """Decorator to redirect if user is missing."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not g.user:
            flash("Please login or sign up to view this feature.", "danger")
            return redirect("/login")
        return func(*args, **kwargs)
    return wrapper

################################################## Authentication Routes ##################################################
@app.route('/login', methods=["GET", "POST"])
def login():
    """Login Route"""
    form = LoginForm()
    if form.is_submitted() and (user := User.authenticate(form.username.data, form.password.data)):
        do_login(user)
        flash(f"Hello, {user.username}!", "success")
        return redirect("/dashboard")
    elif form.is_submitted():
        flash("Invalid credentials.", 'danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    """Logout Route"""
    do_logout()
    flash("You have successfully logged out", "success")
    return redirect(url_for('login'))

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Signup Route"""
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
            do_login(user)
            flash("Signed up successfully", "success")
            return redirect(url_for('dashboard'))
        except IntegrityError:
            flash("Username already taken", 'danger')
    return render_template('signup.html', form=form)

################################################## User Routes ##################################################
@app.route('/')
def homepage():
    return render_template('homepage.html', user=g.user)

@app.route('/profile/<int:user_id>')
@redirect_if_missing
def profile(user_id):
    user = User.query.get_or_404(user_id)
    if g.user.id != user_id:
        flash("You do not have permission to view this page.", "error")
        return redirect(url_for('homepage'))
    return render_template('profile.html', user=user)

@app.route('/edit_profile', methods=['GET', 'POST'])
def edit_profile():
    form = EditProfileForm()

    if form.validate_on_submit():
        # Update user profile data
        g.user.image_url = form.image_url.data
        g.user.username = form.username.data

        # Check if a new password is provided
        if form.password.data:
            g.user.password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')

        g.user.email = form.email.data

        # Commit changes to the database
        db.session.commit()

        flash('Profile updated successfully!', 'success')

        # Redirect to the profile page after a successful update
        return redirect(url_for('profile', user_id=g.user.id))

    # Render the edit_profile template with the form
    return render_template('edit_profile.html', form=form, user=g.user)

@app.route('/delete_account', methods=['POST'])
def delete_account():
    # Check if the user is authenticated
    if g.user:
        # Delete the user and log them out
        db.session.delete(g.user)
        db.session.commit()
        do_logout()
        flash("Your account has been deleted.", "success")
        return redirect(url_for('homepage'))
    else:
        # If the user is not authenticated, redirect to the homepage
        abort(404)

################################################## Data Routes ##################################################
@app.route('/dashboard')
@redirect_if_missing
def dashboard():
    budgets = Budget.query.filter_by(user_id=g.user.id).all()
    savings = Saving.query.filter_by(user_id=g.user.id).all()
    income_categories = set()
    expense_categories = set()

    for budget in budgets:
        for income in budget.income:
            income_categories.add(income.category)

        for expense in budget.expense:
            expense_categories.add(expense.category)

    return render_template('dashboard.html', user=g.user, budgets=budgets, savings=savings)

@app.route('/get-categories', methods=['GET'])
@redirect_if_missing
def get_categories():
    selected_date = request.args.get('date')
    budget = Budget.query.filter_by(user_id=g.user.id, date=selected_date).first()

    if budget:
        income_categories = [income.category for income in budget.income]
        expense_categories = [expense.category for expense in budget.expense]
        return jsonify({'income_categories': income_categories, 'expense_categories': expense_categories})
    else:
        return jsonify({'income_categories': [], 'expense_categories': []})


@app.route('/delete-date', methods=['DELETE'])
@redirect_if_missing
def delete_date():
    selected_date = request.args.get('date')

    try:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except ValueError:
        return 'Invalid date format', 400

    budget = Budget.query.filter_by(user_id=g.user.id, date=selected_date).first()

    if budget:
        try:
            Income.query.filter_by(budget_id=budget.id).delete()
            Expense.query.filter_by(budget_id=budget.id).delete()
            db.session.delete(budget)
            db.session.commit()

            return 'Date deleted successfully', 200
        except Exception as e:
            print(f"Error deleting data for {selected_date}: {e}")
            db.session.rollback()
            return 'Error deleting data for the selected date', 500
    else:
        abort(404)

@app.route('/delete-saving-date', methods=['DELETE'])
@redirect_if_missing
def delete_saving_date():
    selected_saving_date = request.args.get('date')

    try:
        selected_saving_date = datetime.strptime(selected_saving_date, '%Y-%m-%d').date()
    except ValueError:
        return 'Invalid date format', 400

    saving = Saving.query.filter_by(user_id=g.user.id, date=selected_saving_date).first()

    if saving:
        try:
            db.session.delete(saving)
            db.session.commit()

            return 'Saving date deleted successfully', 200
        except Exception as e:
            print(f"Error deleting saving data for {selected_saving_date}: {e}")
            db.session.rollback()
            return 'Error deleting saving data for the selected date', 500
    else:
        abort(404)

@app.route('/budget', methods=["GET", "POST"])
@redirect_if_missing
def budget():
    form = BudgetForm()

    if request.method == "POST":
        date = request.form.get('date')
        user_id = g.user.id
        budget = Budget(user_id=user_id, date=date)
        db.session.add(budget)
        db.session.flush()

        income_categories = request.form.getlist('income_entries[][category]')
        income_amounts = request.form.getlist('income_entries[][amount]')
        expense_categories = request.form.getlist('expense_entries[][category]')
        expense_amounts = request.form.getlist('expense_entries[][amount]')

        process_fields(income_categories, income_amounts, budget, Income)
        process_fields(expense_categories, expense_amounts, budget, Expense)


        db.session.commit()
        flash("Budget data added successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('budget.html', form=form)

def process_fields(categories, amounts, budget, model):
    for category, amount in zip(categories, amounts):
        if amount:
            try:
                amount = float(amount)
                item = model(budget_id=budget.id, category=category, amount=amount)
                db.session.add(item)
            except ValueError:
                flash(f"Invalid amount for {category}. Please enter a valid number.", "danger")

    db.session.commit()

@app.route('/saving', methods=["GET", "POST"])
@redirect_if_missing
def saving():
    form = SavingForm()

    if form.validate_on_submit():
        date = form.date.data
        category = form.category.data
        amount = form.amount.data

        try:
            amount = float(amount)
            saving = Saving(user_id=g.user.id, date=date, category=category, amount=amount)
            db.session.add(saving)
            db.session.commit()
            flash("Savings data added successfully!", "success")
            return redirect(url_for('dashboard'))
        except ValueError:
            flash(f"Invalid amount. Please enter a valid number.", "danger")

    return render_template('saving.html', form=form)

@app.route('/resources')
def resources():
    """Resources Route"""
    return render_template('resources.html', user=g.user)

################################################## API Routes ##################################################
@app.route('/check-auth')
def check_auth():
    is_authenticated = g.user is not None
    return jsonify(isAuthenticated=is_authenticated)

@app.route('/load-data')
@redirect_if_missing
def load_data():
    selected_date = request.args.get('date')
    selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    budget = Budget.query.filter_by(user_id=g.user.id, date=selected_date).first()
    income_data = []
    expense_data = []

    for income in budget.income:
        income_data.append({'category': income.category, 'amount': income.amount})

    for expense in budget.expense:
        expense_data.append({'category': expense.category, 'amount': expense.amount})

    return jsonify({'income': income_data, 'expense': expense_data})

@app.route('/load-saving-data')
@redirect_if_missing
def load_saving_data():
    selected_saving_date = request.args.get('saving-date')
    selected_saving_date = datetime.strptime(selected_saving_date, '%Y-%m-%d').date()

    saving = Saving.query.filter_by(user_id=g.user.id, date=selected_saving_date).first()
    saving_data = []

    if saving:
        print(f"Saving Found - Category: {saving.category}, Amount: {saving.amount}")
        saving_data.append({'category': saving.category, 'amount': saving.amount})

    print(f"Final Saving Data: {saving_data}")

    return jsonify({'saving': saving_data})

@app.route('/about_us')
def about_us():
    return render_template('aboutus.html', user=g.user)

if __name__ == '__main__':
    app.run(debug=True)