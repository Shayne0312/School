from flask import Flask, render_template, redirect, session
from werkzeug.exceptions import Unauthorized
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm, DeleteForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///feedback"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "allofthesecrets"

connect_db(app)

@app.route("/")
def homepage():
    """Homepage redirects to register page."""
    return redirect("/register")

@app.route('/register', methods=['GET', 'POST'])
def register():
    """Produce register form or handle registration."""
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = RegisterForm()
    if form.is_submitted():
        # Handle form submission
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data

        # Register the user
        user = User.register(username, password, email, first_name, last_name)
        db.session.commit()
        session['username'] = user.username

        return redirect(f"/users/{user.username}")
    
    return render_template("users/register.html", form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Produce login form or handle login."""
    if "username" in session:
        return redirect(f"/users/{session['username']}")

    form = LoginForm()
    if form.is_submitted():
        # Handle form submission
        username = form.username.data
        password = form.password.data

        # Authenticate the user
        user = User.authenticate(username, password)
        if user:
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            form.username.errors = ["Invalid username/password."]
            return render_template("users/login.html", form=form)

    return render_template("users/login.html", form=form)

@app.route("/logout")
def logout():
    """Logout route"""
    session.pop("username")
    return redirect("/login")

@app.route("/users/<username>")
def show_user(username):
    """Show user info and feedbacks."""
    if "username" not in session:
        raise Unauthorized()

    # Get the user and feedbacks
    user = User.query.get(username)
    form = DeleteForm()

    return render_template("users/show.html", user=user, form=form)

@app.route("/users/<username>/delete", methods=["POST"])
def remove_user(username):
    """Delete user."""
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    # Delete the user
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    session.pop("username")

    return redirect("/login")

@app.route("/users/<username>/feedback/new", methods=["GET", "POST"])
def new_feedback(username):
    """Show feedback form and process it."""
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    form = FeedbackForm()
    if form.is_submitted() and form.validate():
        # Handle form submission
        title = form.title.data
        content = form.content.data

        # Create new feedback
        feedback = Feedback(title=title, content=content, username=username,)
        db.session.add(feedback)
        db.session.commit()

        return redirect(f"/feedback/{username}")

    return render_template("feedback/new.html", form=form)

@app.route("/feedback/<username>", methods=["GET"])
def show_feedback(username):
    """Show feedback."""
    if "username" not in session or username != session['username']:
        raise Unauthorized()

    # Get the user, form, and feedbacks
    user = User.query.get(username)
    form = DeleteForm()
    feedbacks = Feedback.query.filter_by(username=username)

    return render_template("users/show.html", user=user, form=form, feedbacks=feedbacks)

@app.route("/feedback/<int:feedback_id>/update", methods=["GET", "POST"])
def update_feedback(feedback_id):
    """Show update-feedback form and process it."""
    feedback = Feedback.query.get(feedback_id)
    username = feedback.username

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = FeedbackForm(obj=feedback)
    if form.is_submitted() and form.validate():
        # Handle form submission
        feedback.title = form.title.data
        feedback.content = form.content.data
        db.session.commit()

        return redirect(f"/feedback/{username}")
    else:
        return render_template("/feedback/edit.html", form=form, feedback=feedback)

@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """Delete feedback."""
    feedback = Feedback.query.get(feedback_id)
    username = feedback.username

    if "username" not in session or feedback.username != session['username']:
        raise Unauthorized()

    form = DeleteForm()
    if form.is_submitted():
        # Delete the feedback
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/feedback/{username}")