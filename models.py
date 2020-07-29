"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

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

    def __repr__(self):
        """Show info about the user."""
        return f"<User {self.id} {self.first_name} {self.last_name} {self.image_url}>"