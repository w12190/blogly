"""Blogly application."""
from flask import Flask, render_template, redirect, session, flash, request #TODO delete session if unused
from models import db, connect_db, User, Post, Tag, PostTag
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
                    
    #TODO: add - anytime code runs off screen, insert new lines for arguments 
    # so it doesn't look ugly

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

@app.route('/users/<user_id>')
def show_user_info(user_id):
    """Displays info for a given user."""
    user = User.query.get_or_404(user_id)
    posts = user.posts

    return render_template('user-detail.html', user_in_template = user, 
                            posts_in_template = posts)

@app.route('/users/<user_id>/edit')
def show_user_edit_page(user_id):
    """Displays the user edit page."""
    user = User.query.get_or_404(user_id)
    return render_template('user-edit.html', user_in_template = user)

@app.route('/users/<user_id>/edit', methods=['POST'])
def process_user_edit_form(user_id):
    """ Process the user info edit form, redirects to /users."""
    user = User.query.get_or_404(user_id)

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
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')



# Part 2 Routes
@app.route('/posts/<post_id>')
def show_post(post_id):
    """Show a post."""
    post = Post.query.get_or_404(post_id)
    user = post.user

    return render_template('post-detail.html', user_in_template = user, 
                            post_in_template = post)

@app.route('/posts/<post_id>/edit')
def edit_post(post_id):
    """Show form to edit a post."""
    post = Post.query.get_or_404(post_id)

    return render_template('post-edit.html', post_in_template = post)

@app.route('/posts/<post_id>/edit', methods=['POST'])
def handle_post_edit(post_id):
    """Handle editting of a post, redirect back to the post."""
    post = Post.query.get_or_404(post_id)

    if request.form['post_title'] != '':
        post.title = request.form['post_title']
    if request.form['post_content'] != '':
        post.content = request.form['post_content']

    db.session.commit()

    return redirect('/posts/' + post_id)

@app.route('/posts/<post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Deletes a post."""
    post = Post.query.get_or_404(post_id)
    user = post.user

    db.session.delete(post)
    db.session.commit()

    return redirect('/users/' + str(user.id))

@app.route('/users/<user_id>/posts/new')
def add_post(user_id):
    """Show form to add a post for this user."""
    user = User.query.get_or_404(user_id)
    # TODO: add - use get_or_404 so there's some kind of error checking 
    return render_template('post-add.html', user_in_template = user)


@app.route('/users/<user_id>/posts/new', methods=['POST'])
def handle_add_post(user_id):
    """Handle add form - add new post and redirect to user detail page."""
    new_post = Post(title = request.form['post_title'], 
                    content = request.form['post_content'], user_id = user_id)

    db.session.add(new_post)
    db.session.commit()
    
    return redirect('/users/' + user_id)


    # Third Part

@app.route('/tags')
def show_all_tags():
    """ Lists all tags, with links to the tag detail page """
    tags = Tag.query.order_by(Tag.id).all()
    return render_template('tags.html', tags = tags)

@app.route('/tags/<tag_id>')
def show_tag_detail(tag_id):
    """Show detail about a tag. Display an edit and delete form """
    tag = Tag.query.get_or_404(tag_id)
    posts = tag.posts
    return render_template('tag-detail.html', tag=tag, posts=posts)

@app.route('/tags/new')
def add_tag_form():
    """ Directs to add new tag form """
    return render_template('tag-add.html')

@app.route('/tags/new', methods=['POST'])
def post_new_tag():
    """ Process add form, adds tag, and redirect to tag list. """
    new_tag = Tag(name = request.form['tag_name'])
    print(new_tag)
    db.session.add(new_tag)
    db.session.commit()
    return redirect('/tags')

@app.route('/tags/<tag_id>/edit')
def edit_tag(tag_id):
    """ Show edit form for a tag """
    tag = Tag.query.get_or_404(tag_id)
    return render_template('tag-edit.html', tag=tag)

@app.route('/tags/<tag_id>/edit', methods=['POST'])
def handle_tag_edit(tag_id):
    """ Process edit form, edit tag, and redirects to the tags list. """
    tag = Tag.query.get_or_404(tag_id)
    if request.form['tag_name'] != '':
        tag.name = request.form['tag_name']
    db.session.commit()
    
    return redirect('/tags')

@app.route('/tags/<tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """Deletes a tag and redirects the user to the list of all tags (/tags)"""
    tag = Tag.query.get(tag_id)
    db.session.delete(tag)
    db.session.commit()
    
    return redirect('/tags')