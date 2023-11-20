from flask import Flask, request, render_template, redirect
from models import db, connect_db, User, Post, Tag
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

# ************************************USER**************************************
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
    return redirect(f'/users/{new_user.id}')

@app.route('/users', methods=["GET"])
def list_users():
    """Show a list of all users"""
    users = User.query.all()
    return render_template('list.html', users=users)

@app.route("/users/<int:user_id>")
def show_user(user_id):
    """Show details about a single user"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.filter_by(user_id=user_id).all()
    return render_template("user_details.html", user=user, tags=tags)

@app.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
def edit_user(user_id):
    """Edit user information"""
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url']
        db.session.commit()
        return redirect('/users')

    return render_template('edit_user.html', user=user)

@app.route('/users/<int:user_id>/update', methods=['POST'])
def update_user(user_id):
    """Update user information"""
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    db.session.commit()
    return redirect(f'/users/{user_id}')

@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete a user"""
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

@app.route('/new_user')
def new_user():
    """Show the form to add a new user"""
    return render_template('new_user.html')

# ************************************POST**************************************
@app.route('/users/<int:user_id>/post', methods=['GET', 'POST'])
def create_post(user_id):
    """Create a new post"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.filter_by(user_id=user_id).all()  # Get all tags for the user

    if request.method == 'POST':
        title = request.form["title"]
        content = request.form["content"]
        created_at = datetime.utcnow()
        new_post = Post(title=title, content=content, created_at=created_at, user_id=user_id)

        # Process the selected tags
        for tag in tags:
            if str(tag.id) in request.form.getlist('tags'):
                new_post.tags.append(tag)

        db.session.add(new_post)
        db.session.commit()
        return redirect(f'/users/{user_id}')
    else:
        return render_template('new_post.html', user_id=user_id, tags=tags)

@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show details about a single post"""
    post = Post.query.get_or_404(post_id)
    return render_template('post_details.html', post=post)

@app.route('/users/<int:user_id>/posts/<int:post_id>/edit', methods=['GET', 'POST'])
def edit_post(user_id, post_id):
    """Edit a post"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.filter_by(user_id=user_id).all()  # Get all tags for the user

    if request.method == 'POST':
        if 'title' in request.form:
            post.title = request.form['title']
        if 'content' in request.form:
            post.content = request.form['content']

        # Clear existing tags and add the selected ones
        post.tags.clear()
        for tag in tags:
            if str(tag.id) in request.form.getlist('tags'):
                post.tags.append(tag)

        db.session.commit()
        return redirect(f'/posts/{post_id}')
    else:
        return render_template('edit_post.html', post=post, tags=tags)

@app.route('/users/<int:user_id>/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(user_id, post_id):
    """Delete a post"""
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{user_id}')

# ************************************TAG**************************************

@app.route('/tags/<int:tag_id>')
def show_tag(tag_id):
    """Show details of a tag"""
    tag = Tag.query.get_or_404(tag_id)
    user = User.query.get_or_404(tag.user_id)  # Get the associated user
    return render_template('tag_details.html', tag=tag, user=user)

@app.route('/users/<int:user_id>/add_tags', methods=['GET', 'POST'])
def add_tags(user_id):
    """Add tags for a user"""
    user = User.query.get_or_404(user_id)

    if request.method == 'POST':
        # Process the form submission
        tag_name = request.form['tag_name']
        new_tag = Tag(name=tag_name, user_id=user_id)
        db.session.add(new_tag)
        db.session.commit()
        return redirect(request.referrer)
    else:
        # Render the form
        tags = Tag.query.filter_by(user_id=user_id).all()
        return render_template('add_tags.html', user=user, tags=tags)

@app.route('/tags/new')
def new_tag():
    """Show the form to add a new tag"""
    return render_template('new_tag.html')

@app.route('/tags', methods=['POST'])
def create_tag():
    """Create a new tag"""
    name = request.form['name']
    new_tag = Tag(name=name)
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def update_tag(tag_id):
    """Update a tag"""
    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    db.session.commit()
    return redirect(f'/tags/{tag_id}')

@app.route('/tags/<int:tag_id>/edit', methods=['GET', 'POST'])
def edit_tag(tag_id):
    """Edit a tag"""
    tag = Tag.query.get_or_404(tag_id)

    if request.method == 'POST':
        tag.name = request.form['name']
        db.session.commit()
        return redirect(f'/tags/{tag_id}')

    return render_template('edit_tags.html', tag=tag)

@app.route('/users/<int:user_id>/edit_tags', methods=['GET', 'POST'])
def edit_tags(user_id):
    """Edit tags for a user"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.filter_by(user_id=user_id).all()

    if request.method == 'POST':
        # Process the form submission
        for tag in tags:
            tag_name = request.form.get(f'tag_{tag.id}')
            tag.name = tag_name
            db.session.commit()
        return redirect(f'/users/{user_id}')
    else:
        return render_template('edit_tags.html', user=user, tags=tags)

@app.route('/tags/<int:tag_id>/delete', methods=['GET', 'POST'])
def delete_tag(tag_id):
    """Delete a tag"""
    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    return redirect(f'/users/{tag.user_id}/add_tags')

if __name__ == '__main__':
    app.run(debug=True)