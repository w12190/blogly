"""Blogly application."""
from flask import Flask, render_template, redirect, session, flash, request #TODO delete session if unused
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config['SECRET_KEY'] = "very-secret"
debug = DebugToolbarExtension(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
connect_db(app)
db.create_all()

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
    
    new_user = User(first_name = request.form['first_name'], last_name = request.form['last_name'], image_url = request.form['image_url'])

    db.session.add(new_user)
    db.session.commit()

    return redirect('/users')

# @app.route('/users/<user_id>')
# def show_user_info(user_id):
#     """Displays info for a given user."""
#     return render_template('user-detail.html')

# @app.route('/users/<user_id>/edit')
# def show_user_edit_page(user_id):
#     """Displays the user edit page."""
#     return render_template('user-edit.html')

# @app.route('/users/<user_id>/edit', methods=['POST'])
# def process_user_edit_form(user_id):
#     """ Process the user info edit form, redirects to /users."""
#     return redirect('/users')

# @app.route('/users/<user-id>/delete', methods=['POST'])
# def delete_user():
#     """Delete the given user, redirects to /users."""
#     return redirect('/users')