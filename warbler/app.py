"""Main application"""

import os

from flask import Flask, render_template, request, flash, redirect, session, g # noqa
from sqlalchemy.exc import IntegrityError # noqa

from forms import UserAddForm, LoginForm, UserEditForm, MessageForm
from models import db, connect_db, User, Message, Follows
from functools import wraps

CURR_USER_KEY = "curr_user"

# Configure and Initialize app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = (os.environ.get('DATABASE_URL', 'postgresql:///warbler'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

connect_db(app)

##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


def do_login(user):
    """Log in user."""

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

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup."""

    form = UserAddForm()

    if form.is_submitted() and form.validate():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
                image_url=form.image_url.data or User.image_url.default.arg,
                header_image_url=form.header_image_url.data or User.header_image_url.default.arg,
                bio=form.bio.data or User.bio.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/signup.html', form=form)

        do_login(user)
        return redirect("/")
    else:
        return render_template('users/signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.is_submitted() and form.validate():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    do_logout()
    flash("You have successfully logged out", "success")
    return redirect('/login')


##############################################################################
# General user routes:

@app.route('/users')
def list_users():
    """Page with listing of users.
    Can take a 'q' param in querystring to search by that username.
    """

    search = request.args.get('q')

    if not search:
        users = User.query.all()
    else:
        users = User.query.filter(User.username.like(f"%{search}%")).all()

    return render_template('users/index.html', users=users)


@app.route('/users/<int:user_id>')
def users_show(user_id):
    """Show user profile."""

    user = User.query.get_or_404(user_id)

    messages = (Message
                .query
                .filter(Message.user_id == user_id)
                .order_by(Message.timestamp.desc())
                .limit(100)
                .all())
    return render_template('users/show.html', user=user, messages=messages)

@app.route('/users/<int:user_id>/following')
@redirect_if_missing
def show_following(user_id):
    """Show list of people this user is following."""

    user = User.query.get_or_404(user_id)
    return render_template('users/following.html', user=user)


@app.route('/users/<int:user_id>/followers')
@redirect_if_missing
def users_followers(user_id):
    """Show list of followers of this user."""

    user = User.query.get_or_404(user_id)
    return render_template('users/followers.html', user=user)

@app.route('/users/<int:user_id>/likes')
@redirect_if_missing
def users_likes(user_id):
    """Show list of liked messages for this user."""

    user = User.query.get_or_404(user_id)
    return render_template('users/likes.html',user=user)

@app.route('/users/follow/<int:follow_id>', methods=['POST'])
@redirect_if_missing
def add_follow(follow_id):
    """Add a follow for the currently-logged-in user."""
    
    followed_user = User.query.get(follow_id)  
    if followed_user is None:
        return redirect('/error')
        
    following_user = g.user
        
    follow = Follows(user_being_followed_id=followed_user.id, user_following_id=following_user.id)
                     
    db.session.add(follow)
    db.session.commit()
    
    return redirect(f"/users/{g.user.id}/following")


@app.route('/users/stop-following/<int:follow_id>', methods=['POST'])
@redirect_if_missing
def stop_following(follow_id):
    """Have currently-logged-in-user stop following this user."""

    followed_user = User.query.get(follow_id)
    g.user.following.remove(followed_user)
    db.session.commit()

    return redirect(f"/users/{g.user.id}/following")

@app.route('/users/toggle_like/<int:like_id>', methods=['POST'])
@redirect_if_missing
def add_like(like_id):
    """Toggle like for the currently-logged-in user."""
    
    liked_message = Message.query.get(like_id)
    if liked_message in g.user.likes:
        g.user.likes.remove(liked_message)
    else:
        g.user.likes.append(liked_message)
    db.session.commit()
    if request.referrer:
        return redirect(f"{request.referrer}")
    return redirect('/')

@app.route('/users/profile', methods=["GET", "POST"])
@redirect_if_missing
def profile():
    """Update profile for current user."""

    form = UserEditForm(obj=g.user)
    if form.is_submitted() and form.validate():
        user = User.authenticate(g.user.username,
                                 form.password.data)
        if user:
            user.username = form.username.data
            user.email = form.email.data
            user.image_url = form.image_url.data
            user.header_image_url = form.header_image_url.data
            user.bio = form.bio.data
            db.session.add(user)
            db.session.commit()
            return redirect(f"/users/{user.id}")
        flash('Incorrect password.', "danger")
        return redirect('/')
    return render_template('users/edit.html',form=form)

@app.route('/users/delete', methods=["POST"])
@redirect_if_missing
def delete_user():
    """Delete user."""

    do_logout()

    db.session.delete(g.user)
    db.session.commit()

    flash(f"{g.user.username} has been deleted.", "success")
    return redirect("/signup")


##############################################################################
# Messages routes:

@app.route('/messages/new', methods=["GET", "POST"])
@redirect_if_missing
def messages_add():
    """Add a message:
    Show form if GET. If valid, update message and redirect to user page.
    """

    form = MessageForm()

    if form.is_submitted() and form.validate():
        msg = Message(text=form.text.data)
        g.user.messages.append(msg)
        db.session.commit()
        flash("Message posted", "success")
        return redirect(f"/users/{g.user.id}")

    return render_template('messages/new.html', form=form)


@app.route('/messages/<int:message_id>', methods=["GET", "POST"])
def messages_show(message_id):
    """Show a message."""

    msg = Message.query.get(message_id)
    return render_template('messages/show.html', message=msg)


@app.route('/messages/<int:message_id>/delete', methods=["POST"])
@redirect_if_missing
def messages_destroy(message_id):
    """Delete a message."""
    
    msg = Message.query.get(message_id)
    if msg.user_id != g.user.id:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    db.session.delete(msg)
    db.session.commit()

    return redirect(f"/users/{g.user.id}")


##############################################################################
# Homepage and error pages


@app.route('/')
def homepage():
    """Show homepage:
    - anon users: no messages
    - logged in: 100 most recent messages of followed_users
    """

    if g.user:
        filtered_messages = [f.id for f in g.user.following]
        filtered_messages.append(g.user.id)
        messages = (Message 
                    .query
                    .join(User)
                    .join(Follows, User.id==Follows.user_following_id)
                    .filter(Message.user_id.in_(filtered_messages))
                    .order_by(Message.timestamp.desc())
                    .limit(100)
                    .all())

        return render_template('home.html', messages=messages)

    else:
        return render_template('home-anon.html')

@app.after_request
def add_header(req):
    """Add non-caching headers on every request."""

    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req

if __name__ == "__main__":
    app.run()