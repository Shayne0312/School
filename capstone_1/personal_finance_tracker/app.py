import os
from flask import Flask, render_template, request, flash, redirect, url_for, session, g, jsonify
from sqlalchemy.exc import IntegrityError
from flask_login import current_user, login_user
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

# User signup/login/logout

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
    """Handles auth if not logged in."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not g.user:
            flash("Access unauthorized.", "danger")
            return redirect("/")
        return func(*args, **kwargs)
    return wrapper

# Routes

@app.route('/')
def homepage():
    """Home Page"""
    return render_template('homepage.html', user=g.user)

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""
    form = LoginForm()

    if form.is_submitted() and (user := User.authenticate(form.username.data, form.password.data)):
        do_login(user)
        flash(f"Hello, {user.username}!", "success")
        return redirect("/dashboard")
    elif form.is_submitted():
        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)

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
            return render_template('signup.html', form=form)

        do_login(user)
        print("Signed up successfully")
        return redirect("/")
    return render_template('signup.html', form=form)


@app.route('/check-auth')
def check_auth():
    """Checks if User is logged in"""
    is_authenticated = g.user is not None
    return jsonify(isAuthenticated=is_authenticated)

@app.route('/logout')
def logout():
    """Handles user logout"""
    do_logout()
    flash("You have successfully logged out", "success")
    return redirect(url_for('login'))

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
        return redirect(url_for('homepage'))

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

@app.route('/dashboard')
@redirect_if_missing
def dashboard():
    # Load budgets for the current user
    budgets = Budget.query.filter_by(user_id=g.user.id).all()

    # Calculate totals
    total_income = db.session.query(db.func.sum(Income.amount)).\
                    filter(Income.budget_id.in_([b.id for b in budgets])).\
                    scalar()
    total_expense = db.session.query(db.func.sum(Expense.amount)).\
                   filter(Expense.budget_id.in_([b.id for b in budgets])).\
                   scalar()
    net_total = total_income - total_expense

    return render_template('dashboard.html', user=g.user, budgets=budgets, total_income=total_income,
                           total_expense=total_expense, net_total=net_total)


@app.route('/budget', methods=["GET", "POST"])
@redirect_if_missing
def budget():
    form = BudgetForm()
    if request.method == "POST":
        # Create a new budget instance
        date = request.form.get('date')
        user_id = g.user.id
        budget = Budget(user_id=user_id, date=date)
        db.session.add(budget)
        db.session.flush()  # This will assign an ID to the budget without committing the transaction

        # Process income fields
        income_categories = ['salary_income_category', 'other_income_category']
        for category_field in income_categories:
            category = request.form.get(category_field)
            amount_field = category_field.replace('category', 'amount')
            amount = float(request.form.get(amount_field, 0))
            income = Income(budget_id=budget.id, category=category, amount=amount)
            db.session.add(income)

        # Process expense fields
        expense_categories = ['housing_expense_category', 'other_expense_category']
        for category_field in expense_categories:
            category = request.form.get(category_field)
            amount_field = category_field.replace('category', 'amount')
            amount = float(request.form.get(amount_field, 0))
            expense = Expense(budget_id=budget.id, category=category, amount=amount)
            db.session.add(expense)

        # Commit all changes to the database
        db.session.commit()
        flash("Budget data added successfully!", "success")
        return redirect(url_for('dashboard'))

    return render_template('budget.html', form=form)


@app.route('/saving', methods=["GET", "POST"])
def saving():
    """Savings Page."""
    if not g.user:
        flash("Please sign in to view this page.", "error")
        return redirect(url_for('login'))

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

if __name__ == '__main__':
     app.run(debug=True)