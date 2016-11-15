"""ADU bento box."""

import os

from flask import (Flask, render_template, redirect, request, session, flash)
# from flask_debugtoolbar import DebugToolbarExtension

from model import db, connect_to_db
from model import (User, Flashcard, Content)

import bcrypt


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

    user_id = session.get('current_user')

    if not user_id:
        return redirect("/login")
    else:
        return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def user_register():
    """User register form."""
    return render_template("register.html")


@app.route('/login', methods=['GET'])
def user_login():
    """User login form."""
    return render_template("login.html")


@app.route('/register', methods=['POST'])
def register_process():
    """Process new user account registration; user entered into database."""

    # In case form not fully filled out.
    email, password, age, zipcode, architecture_degree = '', '', 0, '00000', False

    # Get form variables.
    email = request.form['email']
    password = request.form['password']
    age = request.form['age']
    zipcode = request.form['zipcode']
    architecture_degree = request.form['architecture_degree']

    if User.query.filter_by(email=email).first():  # Checks to see if user is already registered.
        flash("You're already registered. Please log in.")
        return redirect('/')
    else:
        # Hash a password for the first time, with a randomly-generated salt.
        p = password.encode()
        hashed = bcrypt.hashpw(p, bcrypt.gensalt())
        new_user = User(email=email, password=hashed, age=age, zipcode=zipcode, architecture_degree=architecture_degree)

        db.session.add(new_user)
        db.session.commit()

        session['current_user'] = email
        flash("Welcome, %s! You are now registered." % (email))
        return render_template("homepage.html")


@app.route('/login', methods=['POST'])
def login_process():
    """Process user login; user login to be completed."""

    # Get form variables.
    email = request.form['email']
    password = request.form['password']

    user = User.query.filter_by(email=email).first()
    hashed = user.password

    if user:  # Checks to see if user is registered.
        # # Checks to see if user password is correct (not using bcrypt hashing).
        # if current_password == user.password:

        # Check that an unhashed password matches one that has previously been hashed.
        if bcrypt.checkpw(password, hashed):
            session['current_user'] = email
            flash("Logged in as %s" % (email))
            return render_template("homepage.html")
        else:
            flash("Wrong password. Try again!")
            return redirect('/login')
    else:
        flash("Please register.")
        return redirect('/register')


@app.route('/logout', methods=['POST'])
def process_logout():
    """Identifies user session to be deleted. Deletes user session. Redirects."""

    current_user = session['current_user']
    del session['current_user']
    flash("You have logged out, %s." % current_user)
    return redirect('/')


@app.route('/color')
def pick_color():
    return render_template("colorpicker.html")


@app.route('/slider')
def pick_opacity():
    return render_template("slider.html")


#################################
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
    db.create_all()

    DEBUG = "NO_DEBUG" not in os.environ
    PORT = int(os.environ.get("PORT", 5000))

    app.run(host="0.0.0.0", port=PORT, debug=DEBUG)
