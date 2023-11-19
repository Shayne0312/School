from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post
from datetime import datetime

app = Flask(__name__)

# Configure the app
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"

# Connect to the database
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
        user.image_url = request.form['image_url']
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
    
    return redirect('{{user_id}')  # Redirect to home page if not a POST request

@app.route('/new_user')
def new_user():
    """Render the new user form"""
    return render_template('new_user.html')

@app.route('/users/<int:user_id>/post') 
def new_post(user_id): 
    """Render the new post form""" 
    return render_template('post.html', user_id=user_id)

@app.route('/users/<int:user_id>/post', methods=['GET', 'POST'])
def create_post(user_id):
    """Create a new post"""
    if request.method == 'POST':
        title = request.form["title"]
        content = request.form["content"]
        created_at = datetime.utcnow()  # Get the current date and time
        
        new_post = Post(title=title, content=content, created_at=created_at, user_id=user_id)
        db.session.add(new_post)
        db.session.commit()
        
        return redirect(f'/{user_id}')
    else:
        return render_template('post.html', user_id=user_id)

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show details about a single post"""
    post = Post.query.get_or_404(post_id)
    return render_template('post_details.html', post=post)

@app.route('/users/<int:user_id>/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(user_id, post_id):
    """Edit a post"""
    post = Post.query.get_or_404(post_id)
    
    if request.method == 'POST':
        # Process the form data and update the post
        post.title = request.form['title']
        post.content = request.form['content']
        db.session.commit()
        
        return redirect(f'/{user_id}')
    
    return render_template('edit_post.html', post=post)

@app.route('/users/<int:user_id>/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(user_id, post_id):
    """Delete a post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    
    return redirect(f'/{user_id}')

if __name__ == '__main__':
    app.run(debug=True)