import os
from flask import Flask, render_template, request, flash, redirect, url_for, session, g, jsonify, abort
from sqlalchemy.exc import IntegrityError
from flask_bcrypt import Bcrypt
from datetime import datetime
from forms import LoginForm, SignupForm, EditProfileForm, BudgetForm, SavingForm
from models import db, connect_db, User, Budget, Saving, Income, Expense
from functools import wraps

CURR_USER_KEY = "curr_user"
bcrypt = Bcrypt()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'postgresql:///finance')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', "secretkey")

connect_db(app)

################################################## Helper Functions ##################################################
@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    g.user = User.query.get(session.get(CURR_USER_KEY)) if CURR_USER_KEY in session else None
    print("User is authenticated:", g.user.is_authenticated if g.user else None)

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
    """Homepage Route"""
    return render_template('homepage.html', user=g.user)

@app.route('/profile/<int:user_id>')
@redirect_if_missing
def profile(user_id):
    """Profile Route"""
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

        # Redirect to the profile page after successful update
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
    """Dashboard Route"""
    budgets = []  # List of budgets for the current user
    # Get all budgets for the current user
    budgets = Budget.query.filter_by(user_id=g.user.id).all()
    # Get all savings goals for the current user
    savings_goals = Saving.query.filter_by(user_id=g.user.id).all()
    # Get distinct income categories
    income_categories = set()
    for budget in budgets:
        for income in budget.income:
            income_categories.add(income.category)
    # Get distinct expense categories
    expense_categories = set()
    for budget in budgets:
        for expense in budget.expense:
            expense_categories.add(expense.category)
    return render_template('dashboard.html', user=g.user, budgets=budgets,
                           income_categories=sorted(income_categories),
                           expense_categories=sorted(expense_categories),
                           savings_goals=savings_goals)

@app.route('/delete-date', methods=['DELETE'])
@redirect_if_missing
def delete_date():
    selected_date = request.args.get('date')

    # Check if the selected date is in the correct format
    try:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except ValueError:
        return 'Invalid date format', 400

    # Find the budget associated with the selected date and the current user
    budget = Budget.query.filter_by(user_id=g.user.id, date=selected_date).first()

    if budget:
        try:
            # Delete associated income records
            Income.query.filter_by(budget_id=budget.id).delete()

            # Delete associated expense records
            Expense.query.filter_by(budget_id=budget.id).delete()

            # Delete the budget
            db.session.delete(budget)
            db.session.commit()

            return 'Date deleted successfully', 200
        except Exception as e:
            print(f"Error deleting data for {selected_date}: {e}")
            db.session.rollback()
            return 'Error deleting data for the selected date', 500
    else:
        # If no budget found for the selected date, return a 404 response
        abort(404)

@app.route('/budget', methods=["GET", "POST"])
@redirect_if_missing
def budget():
    form = BudgetForm()

    if request.method == "POST":
        print(request.form)
    
        date = request.form.get('date')
        user_id = g.user.id
        budget = Budget(user_id=user_id, date=date)
        db.session.add(budget)
        db.session.flush()

        # Process income fields
        income_categories = request.form.getlist('income_entries[][category]')
        income_amounts = request.form.getlist('income_entries[][amount]')
        print("Income categories:", income_categories)
        print("Income amounts:", income_amounts)
        process_fields(income_categories, income_amounts, 'income', budget, Income)

        # Process expense fields
        expense_categories = request.form.getlist('expense_entries[][category]')
        expense_amounts = request.form.getlist('expense_entries[][amount]')
        print("Expense categories:", expense_categories)
        print("Expense amounts:", expense_amounts)
        process_fields(expense_categories, expense_amounts, 'expense', budget, Expense)

        db.session.commit()
        flash("Budget data added successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('budget.html', form=form)



def process_fields(categories, amounts, prefix, budget, model):
    for category, amount in zip(categories, amounts):
        print(f"Processing {prefix} entry - Category: {category}, Amount: {amount}")

        if amount:  # Proceed only if amount is not empty
            try:
                amount = float(amount)  # Attempt to convert to float
                item = model(budget_id=budget.id, category=category, amount=amount)
                db.session.add(item)
                print(f"Added {prefix} record to the database.")
            except ValueError:
                flash(f"Invalid amount for {category}. Please enter a valid number.", "danger")
                print(f"Error processing {prefix} entry - Invalid amount.")
                # Handle the exception or log an error message if needed
                pass

    print(f"Finished processing {prefix} entries.")


@app.route('/savings', methods=['GET', 'POST'])
@redirect_if_missing
def savings():
    """Savings Route"""
    if request.method == 'POST':
        form = SavingForm(request.form)
        if form.validate():
            goal_date = form.goal_date.data
            goal_name = form.goal_name.data
            goal_amount = form.goal_amount.data

            # Create a new Saving instance
            saving_goal = Saving(
                user_id=g.user.id,
                date=goal_date,
                name=goal_name,
                amount=goal_amount
            )

            db.session.add(saving_goal)
            db.session.commit()

            flash("Savings goal added successfully!", "success")
            return jsonify({'success': True})

    # If the request method is not POST or form validation fails, retrieve savings goals
    savings_goals = Saving.query.filter_by(user_id=g.user.id).all()

    return render_template('savings.html', user=g.user, savings_goals=savings_goals, form=SavingForm())


################################################## API Routes ##################################################
@app.route('/check-auth')
def check_auth():
    """Checks if User is logged in"""
    is_authenticated = g.user is not None
    return jsonify(isAuthenticated=is_authenticated)

@app.route('/load-data')
@redirect_if_missing
def load_data():
    """Handles loading budget and saving data"""
    selected_date = request.args.get('date')
    # Convert the selected date to a datetime object
    selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    # Use cast to ensure proper date comparison
    budget = Budget.query.filter_by(user_id=g.user.id, date=selected_date).first()
    # Retrieve income and expense data for the selected date
    income_data = []
    expense_data = []
    for income in budget.income:
        income_data.append({'category': income.category, 'amount': income.amount})
    for expense in budget.expense:
        expense_data.append({'category': expense.category, 'amount': expense.amount})
    return jsonify({'income': income_data, 'expense': expense_data})

@app.route('/load-savings-data')
@redirect_if_missing
def load_savings_data():
    print("Loading savings data...")
    selected_date = request.args.get('date')
    # Convert the selected date to a datetime object
    selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    # Query the Saving model to retrieve savings data for the selected date
    savings_data = Saving.query.filter_by(user_id=g.user.id, date=selected_date).all()
    # Convert the data to a format suitable for JSON response
    savings_list = [{'name': saving.name, 'amount': saving.amount} for saving in savings_data]
    print("Savings data loaded successfully:", savings_list)
    return jsonify({'saving': savings_list})

if __name__ == '__main__':
     app.run(debug=True)

