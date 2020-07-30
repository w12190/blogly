"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

def connect_db(app):
        """Connect to database."""

        db.app = app
        db.init_app(app)

class User(db.Model):
    """Model for users in Blogly."""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    first_name = db.Column(db.String(50),
                    nullable = False)
    last_name = db.Column(db.String(50),
                    nullable = False)
    image_url = db.Column(db.String,
                    nullable = False,
                    default = "https://i.stack.imgur.com/l60Hf.png")

    #Relationship setup
    posts = db.relationship('Post', backref='user')

    def __repr__(self):
        """Show info about the user."""
        return f"<User {self.id} {self.first_name} {self.last_name} {self.image_url}>"

class Post(db.Model):
    """Model for posts in Blogly."""

    __tablename__ = "posts"

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    title = db.Column(db.String,
                    nullable = False)
    content = db.Column(db.String, #TODO fix bug if no limit causes problems
                    nullable = False)
    created_at = db.Column(db.DateTime,
                    nullable = False, #TODO change to False if time always required (should be)
                    default = datetime.datetime.utcnow) #TODO fix if it throws issues
    user_id = db.Column(db.Integer,
                        db.ForeignKey("users.id"),
                        nullable = False)

    def __repr__(self):
        """Show info about the post."""
        return f"<Post {self.id} {self.title} {self.content} {self.created_at} {self.user_id}>"

class Tag(db.Model):
    """Model for tags in Blogly."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer,
                    primary_key = True,
                    autoincrement = True)
    name = db.Colum(db.String,
                    nullable = False)

class PostTag(db.Model):
    """Model for post-tag records in Blogly."""

    __tablename__ = 'posts_tags'

    post_id = db.Column(db.Integer,
                    primary_key = True,
                    db.ForeignKey("posts.id"))
    tag_id = db.Column(db.Integer,
                    primary_key = True,
                    db.ForeignKey("users.id"))