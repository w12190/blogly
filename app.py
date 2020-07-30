"""Blogly application."""
from flask import Flask, render_template, redirect, session, flash, request #TODO delete session if unused
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "very-secret"
# debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
connect_db(app)
db.create_all()



#Part 1 Routes

@app.route('/')
def show_homepage():
    """Show the Blogly homepage."""
    return redirect('/users')

@app.route('/users')
def show_users():
    """Display the list of all users."""
    all_users = User.query.all()
    return render_template('users.html', users_in_template = all_users)

@app.route('/users/new')
def show_new_user_form():
    """Display the form to add a new user."""

    return render_template('user-new.html') 

@app.route('/users/new', methods = ['POST'])
def process_new_user_form():
    """Process the form to add a new user, redirects to /users."""
    
    new_user = User(first_name = request.form['first_name'],
                    last_name = request.form['last_name'],
                    image_url = request.form['image_url'])
                    
    #TODO: add - anytime code runs off screen, insert new lines for arguments so it doesn't look ugly

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<user_id>')
def show_user_info(user_id):
    """Displays info for a given user."""
    user = User.query.get(user_id)
    posts = user.posts

    return render_template('user-detail.html', user_in_template = user, posts_in_template = posts)

@app.route('/users/<user_id>/edit')
def show_user_edit_page(user_id):
    """Displays the user edit page."""
    user = User.query.get(user_id)
    return render_template('user-edit.html', user_in_template = user)

@app.route('/users/<user_id>/edit', methods=['POST'])
def process_user_edit_form(user_id):
    """ Process the user info edit form, redirects to /users."""
    user = User.query.get(user_id)

    if request.form['first_name'] != '':
        user.first_name = request.form['first_name']
    if request.form['last_name'] != '':
        user.last_name = request.form['last_name']
    if request.form['image_url'] != '':
        user.image_url = request.form['image_url']
    db.session.add(user)
    db.session.commit()
    return redirect('/users')

@app.route('/users/<user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Delete the given user, redirects to /users."""
    user = User.query.get(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')



# Part 2 Routes
@app.route('/posts/<post_id>')
def show_post(post_id):
    """Show a post."""
    post = Post.query.get(post_id)
    user = post.user

    return render_template('post-detail.html', user_in_template = user, post_in_template = post)

@app.route('/posts/<post_id>/edit')
def edit_post(post_id):
    """Show form to edit a post."""
    post = Post.query.get(post_id)

    return render_template('post-edit.html', post_in_template = post)

@app.route('/posts/<post_id>/edit', methods=['POST'])
def handle_post_edit(post_id):
    """Handle editting of a post, redirect back to the post."""
    post = Post.query.get(post_id)

    if request.form['post_title'] != '':
        post.title = request.form['post_title']
    if request.form['post_content'] != '':
        post.content = request.form['post_content']

    db.session.commit()

    return redirect('/posts/' + post_id)

@app.route('/posts/<post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Deletes a post."""
    post = Post.query.get(post_id)
    user = post.user

    db.session.delete(post)
    db.session.commit()

    return redirect('/users/' + str(user.id))

@app.route('/users/<user_id>/posts/new')
def add_post(user_id):
    """Show form to add a post for this user."""
    user = User.query.get(user_id)
    # TODO: add - use get_or_404 so there's some kind of error checking 
    return render_template('post-add.html', user_in_template = user)


@app.route('/users/<user_id>/posts/new', methods=['POST'])
def handle_add_post(user_id):
    """Handle add form - add new post and redirect to user detail page."""
    new_post = Post(title = request.form['post_title'], content = request.form['post_content'], user_id = user_id)

    db.session.add(new_post)
    db.session.commit()
    
    return redirect('/users/' + user_id)