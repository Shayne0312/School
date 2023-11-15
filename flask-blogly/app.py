from flask import Flask, request, render_template, redirect
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"

with app.app_context():
    connect_db(app)
    db.create_all()

@app.route('/')
def home():
    """Home page"""
    return redirect('/users')

@app.route('/', methods=["POST"])
def create_user():
    """Create a new user"""
    first_name = request.form["first_name"]
    last_name = request.form["last_name"]
    url = request.form["URL"]
    new_user = User(first_name=first_name, last_name=last_name, image_url=url)
    db.session.add(new_user)
    db.session.commit()
    return redirect(f'/{new_user.id}')

@app.route('/users', methods=["GET"])
def list_users():
    """Show a list of all users"""
    users = User.query.all()
    return render_template('list.html', users=users)

@app.route("/<int:user_id>")
def show_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    """Edit user information"""
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        # Process the form data and update the user's information
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url']  # Fix the field name
        db.session.commit()
        return redirect('/users')  # Update the redirect URL
    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete a user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')  # Update the redirect URL

@app.route('/users/<int:user_id>/update', methods=['POST'])
def update_user(user_id):
    """Update user information"""
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        # Process the form data and update the user's information
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url']
        db.session.commit()
        return redirect('/users')  # Update the redirect URL
    return redirect('/')  # Redirect to home page if not a POST request

@app.route('/new_user')
def new_user():
    """Render the new user form"""
    return render_template('new_user.html')

if __name__ == '__main__':
    app.run(debug=True)