import os
from flask import Flask, render_template, request, flash, redirect, url_for, session, g, jsonify
from sqlalchemy.exc import IntegrityError
from flask_login import current_user
from datetime import datetime
from forms import LoginForm, SignupForm, EditProfileForm, BudgetForm
from models import db, connect_db, User, Budget, SavingsGoal, Income, Expense
from functools import wraps

CURR_USER_KEY = "curr_user"

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
@redirect_if_missing
def edit_profile():
    form = EditProfileForm(obj=current_user)
    if form.validate_on_submit():
        form.populate_obj(current_user)
        db.session.commit()
        flash('Profile Updated')
        return redirect(url_for('profile', user_id=current_user.id))
    return render_template('edit_profile.html', form=form)

################################################## Data Routes ##################################################
@app.route('/dashboard')
@redirect_if_missing
def dashboard():
    """Dashboard Route"""
    budgets = []  # List of budgets for the current user
    # Get all budgets for the current user
    budgets = Budget.query.filter_by(user_id=g.user.id).all()
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
                           expense_categories=sorted(expense_categories))

@app.route('/budget', methods=["GET", "POST"])
@redirect_if_missing
def budget():
    """budget Route"""
    form = BudgetForm()

    if request.method == "POST":
        # Create a new budget instance
        date = request.form.get('date')
        user_id = g.user.id
        budget = Budget(user_id=user_id, date=date)
        db.session.add(budget)
        # Assign ID to budget without committing
        db.session.flush()  

        # Process income fields
        income_categories = [
            'salary_income_category', 'overtime_income_category', 'freelance_income_category',
            'investment_income_category', 'alimony_child_support_income_category', 'rental_property_income_category',
            'social_security_pension_income_category', 'royalties_income_category', 'part_time_job_income_category',
            'business_income_category']

        for category_field in income_categories:
            category = request.form.get(category_field)
            amount_field = category_field.replace('category', 'amount')
            amount = request.form.get(amount_field)

            if category and amount:
                # Both category and amount are provided, add to the session
                income = Income(budget_id=budget.id, category=category, amount=float(amount))
                db.session.add(income)

        # Process expense fields
        expense_categories = [
            'housing_expense_category', 'utilities_expense_category', 'food_expense_category', 
            'dining_out_expense_category', 'transportation_expense_category', 'health_insurance_expense_category', 
            'other_insurance_expense_category', 'loan_payments_expense_category', 'entertainment_expense_category', 
            'other_expense_category']

        for category_field in expense_categories:
            category = request.form.get(category_field)
            amount_field = category_field.replace('category', 'amount')
            amount = request.form.get(amount_field)

            if category and amount:
                # Both category and amount are provided, add to the session
                expense = Expense(budget_id=budget.id, category=category, amount=float(amount))
                db.session.add(expense)

        # Commit the changes to the database
        db.session.commit()
        flash("Budget data added successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('budget.html', form=form)


@app.route('/saving', methods=["GET", "POST"])
def saving():
    """Saving Route"""
    if request.method == "POST":
        # Process the savings goal form data and save it to the database
        process_savings_goal_form(request.form, g.user.id)
        flash("Savings goal added successfully!", "success")
        return redirect(url_for('dashboard'))
    return render_template('saving.html', user=g.user)

def load_savings_goals_for_user(user_id):
    """Loads savings goals for the user."""
    savings_goals = SavingsGoal.query.filter_by(user_id=user_id).all()
    return savings_goals

def process_savings_goal_form(form_data, user_id):
    """Processes the savings goal form data and saves it to the database."""
    new_savings_goal = SavingsGoal(user_id=user_id, **form_data)
    db.session.add(new_savings_goal)
    db.session.commit() 

################################################## API Routes ##################################################
@app.route('/check-auth')
def check_auth():
    """Checks if User is logged in"""
    is_authenticated = g.user is not None
    return jsonify(isAuthenticated=is_authenticated)

@app.route('/load-data')
@redirect_if_missing
def load_data():
    """Handles loading budget data"""
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

if __name__ == '__main__':
     app.run(debug=True)