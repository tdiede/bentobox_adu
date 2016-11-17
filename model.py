"""Models and database functions for BENTO BOX project."""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import postgresql

# This is the connection to the PostgreSQL database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing).

db = SQLAlchemy()


##############################################################################
# Model definitions

class User(db.Model):
    """User of website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)

    email = db.Column(db.String(64), nullable=True, unique=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(10), nullable=True)
    architecture_degree = db.Column(db.Boolean, nullable=True)

    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<User user_id=%d email=%s>" % (self.user_id, self.email)


class Component(db.Model):
    """Categories of components users can select for ADU customization."""

    __tablename__ = "components"

    component_id = db.Column(db.Integer,
                             autoincrement=True,
                             primary_key=True)

    category = db.Column(db.String(128), nullable=False)
    component = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<Component category=%s component=%s>" % (self.category, self.component)


class Option(db.Model):
    """Options that a user has saved to profile."""

    __tablename__ = "options"

    option_id = db.Column(db.Integer,
                          autoincrement=True,
                          primary_key=True)

    user_id = db.Column(db.Integer,
                        db.ForeignKey('users.user_id'))
    selections = db.Column(postgresql.JSON)

    def __repr__(self):
        """Provides helpful representation when printed."""

        return "<Option option_id=%d selections=%s>" % (self.option_id, self.selections)


# class Flashcard(db.Model):
#     """Flashcards made from Content, stored under User profile."""

#     __tablename__ = "flashcards"

#     flashcard_id = db.Column(db.Integer,
#                              autoincrement=True,
#                              primary_key=True)
#     user_id = db.Column(db.Integer,
#                         db.ForeignKey('users.user_id'))
#     content_id = db.Column(db.Integer,
#                            db.ForeignKey('contents.content_id'))

#     # Define relationship to user.
#     user = db.relationship("User",
#                            backref=db.backref("flashcards",
#                                               order_by=flashcard_id))

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         return "<Flashcard flashcard_id=%s name=%s>" % (self.flashcard_id, self.name)


# class Content(db.Model):
#     """Content of flashcards."""

#     __tablename__ = "contents"

#     content_id = db.Column(db.Integer,
#                            autoincrement=True,
#                            primary_key=True)
#     title = db.Column(db.String(128))
#     question = db.Column(db.String(256))
#     answer = db.Column(db.String(256))
#     img = db.Column(db.String(256))
#     category = db.Column(db.String(128))

#     def __repr__(self):
#         """Provide helpful representation when printed."""

#         s = "<Content content_id=%s title=%s question=%s answer=%s>"
#         return s % (self.content_id, self.title, self.question, self.answer)


##############################################################################
# Helper functions

def connect_to_db(app, db_uri=None):
    """Connect the database to our Flask app."""

    # Configure to use our PstgreSQL database
    app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'postgresql:///components'
    # app.config['SQLALCHEMY_DATABASE_URI'] = db_uri or 'postgresql:///flashcards'
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."
