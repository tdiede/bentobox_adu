"""ADU bento box."""

import os

from flask import (Flask, render_template, request, flash)
from flask import redirect, session as flask_session
# from flask_debugtoolbar import DebugToolbarExtension

from model import db, connect_to_db
from model import (User, Flashcard, Content)


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("FLASK_SECRET_KEY", "abcdef")

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
# from jinja2 import StrictUndefined
# app.jinja_env.undefined = StrictUndefined


@app.route("/error")
def error():
    raise Exception("Error!")


@app.route('/')
def index():
    """Homepage."""

    num = flask_session["visits"] = flask_session.get("visits", 0) + 1
    return render_template("homepage.html", num=num)


@app.route('/register', methods=['GET'])
def register_form():
    """New users can create an account through this form."""

    return render_template("register_form.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process new user account registration."""

    # Get form variables.
    email = request.form['email']
    password = request.form['password']
    age = int(request.form['age'])
    zipcode = request.form['zipcode']

    new_user = User(email=email, password=password, age=age, zipcode=zipcode)

    db.session.add(new_user)
    db.session.commit()

    flash("User %s added." % email)
    return redirect("/")


@app.route('/login', methods=['GET'])
def login_form():
    """Registered users can log in through this form."""

    return render_template("login_form.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process user login."""

    # Get form variables.
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()

    if not user:
        flash("You are not a registered user, %s. Please register." % email)
        return redirect("/register")

    if user.password != password:
        flash("Incorrect password. Please try again.")
        return redirect("/login")

    session['user_id'] = user.user_id

    flash("Logged in.")
    return redirect("/users/%s" % user.user_id)


@app.route('/logout', methods=['POST'])
def logout_process():
    """Process user logout."""

    del session['user_login']
    flash('You are now logged out.')
    return redirect("/")


@app.route('/users')
def user_list():
    """Show list of users."""

    users = User.query.all()

    return render_template("user_list.html", users=users)


@app.route('/users/<int:user_id>')
def user_profile(user_id):
    """Show user profile and information."""

    user = User.query.get(user_id)
    return render_template("user.html", user=user)


@app.route('/flashcards')
def show_flashcards():
    """Show list of flashcards."""

    flashcards = Flashcard.query.order_by('name').all()

    return render_template("flashcards.html", flashcards=flashcards)


@app.route('/flashcards/<int:flashcard_id>', methods=['GET'])
def test_flashcard(flashcard_id):

    flashcard = Flashcard.query.get(flashcard_id)

    return render_template("flashcard.html",
                           flashcard=flashcard)


@app.route('/flashcards/<int:flashcard_id>', methods=['POST'])
def make_flashcard(flashcard_id):
    """Add (or edit) a flashcard."""

    # Get form variables.
    content_id = int(request.form['content_id'])
    knowledge_score = int(request.form['knowledge_score'])

    user_id = session.get('user_id')
    if not user_id:
        raise Exception("No user logged in.")

    content = Content.query.filter_by(content_id).first()
    flashcard = Flashcard(user_id=user_id, content=content, knowledge_score=knowledge_score)
    flash('Flashcard added to your deck.')
    db.session.add(flashcard)
    db.session.commit()

    return redirect("/flashcards/%s" % flashcard_id)


################################################################################

if __name__ == "__main__":
    # We have to set debug=True here, at the point we invoke the DebugToolbarExtension.
    # app.debug = True
    # app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    # DebugToolbarExtension(app)

    connect_to_db(app, os.environ.get("DATABASE_URL"))

    # Create the tables we need from our models (if they don't already exist).
    db.create_all(app=app)

    DEBUG = "NO_DEBUG" not in os.environ
    PORT = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
