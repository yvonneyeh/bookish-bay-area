"""Server for Bookish Bay Area app."""

import os
from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import (db, connect_to_db, User, Book, Rating, Author, BookAuthor, Genre, BookGenre, Location, BookLocation)
from sqlalchemy_searchable import search
from datetime import date, datetime
from random import randint
import faker
import crud
import helper

from jinja2 import StrictUndefined

MAPS_JS_KEY = os.environ['MAPS_JS_KEY']

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


# ---------- ACCOUNT ROUTES ---------- #

@app.route("/register")
def reg_form():
    """Display registration form"""

    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_user():
    """Creates new user if user does not yet exist"""

    username = request.form.get("username")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    # Validate if username or email already exists in users table in database
    if not crud.get_user_by_email_id(email, username):

        user = User(username=username, email=email, first_name=first_name, last_name=last_name, password=password)

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("User created!")

        return redirect("/login")

    # If account does exist, flash message to indicating email or username exists.
    else:
        if User.query.filter_by(email=email).all():
            flash(f"There's already an account associated with {email}")
        else:
            flash(f"The username {username} is already taken")

        return redirect("/register")


@app.route('/login')
def login():
    """View Login page."""

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def log_in_user():
    """Login user and redirect to homepage."""

    username = request.form.get('username')
    password = request.form.get('password')

    user_object = crud.get_user_by_id(username)

    if user_object != None:
        if password == user_object.password != None:
            session['username'] = user_object.username
            session['user_id'] = user_object.user_id
            # print('Logged in!')
            flash('Logged in!')
        else:
            flash('Incorrect password') 
            return redirect("/login")  
    else:
        flash('Username does not exist. Please register for an account.')
        return redirect("/register")
    
    return redirect('/')


@app.route("/account/update_info")
def show_acct_info_form():
    """Display form for user to update account information"""

    if "user_id" in session:
        user = User.query.get(session.get("user_id"))

        return render_template("/user_info.html", user=user)

    else:
        flash("You need to be logged in to access that page")

        return redirect("/login")


@app.route("/account/update_info", methods=["POST"])
def update_account_info():
    """Update a user's account information"""

    if "user_id" in session:
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        username = request.form.get("username")
        email = request.form.get("email")
        bio = request.form.get("bio")
        
        user = User.query.get(session["user_id"])

        # Form fields are not required - only update database if text was
        # entered in that field and not the same as what's already in the db
        if len(first_name) > 0 and first_name != user.first_name:
            user.first_name = first_name

        if len(last_name) > 0 and last_name != user.last_name:
            user.last_name = last_name

        if len(username) > 0 and username != user.username:
            user.username = username

        if len(email) > 0 and email != user.email:
            user.email = email

        if len(bio) > 0 and bio != user.bio:
            user.bio = bio

        db.session.add(user)
        db.session.commit()

        flash("Information updated!")

        return redirect("/account/update_info")

    else:
        flash("You need to be logged in to access that page")

        return redirect("/login")


@app.route("/account/change_password")
def show_change_pass_form():
    """Show form for users to change their password"""

    if "user_id" in session:
        return render_template("update_password.html")

    else:
        flash("You need to be logged in to access that page")
        return redirect("/login")

@app.route("/account/change_password", methods=["POST"])
def change_user_password():
    """Change a user's password"""

    if "user_id" in session:
        old_pass = request.form.get("oldpass")
        new_pass = request.form.get("newpass")

        user = User.query.get(session["user_id"])

        if user.check_password(old_pass):
            user.set_password(new_pass)

            db.session.add(user)
            db.session.commit()

            flash("Password successfully updated")

            return redirect("/account/change_password")

        else:
            flash("Incorrect password, please try again")

            return redirect("/account/change_password")

    else:
        flash("You need to be logged in to access that page")

        return redirect("/login")


@app.route("/account/saved_books")
def display_saved_books():
    """Display a user's saved books"""

    if "username" in session:
        username = session.get("username")
        ratings = crud.get_user_ratings(username)

        return render_template("user_books.html",
                               ratings=ratings)

    else:
        flash("You need to be logged in to access that page")

        return redirect("/login")


@app.route('/users')
def all_users():
    """Display all users."""
    users = crud.get_all_users()

    return render_template("all_users.html", users=users)


@app.route('/users', methods=['POST'])
def create_account():
    """Create a new user account."""

    username = request.form.get('username')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')
    join_date = datetime.today()

    if crud.get_user_by_email(email) != None:
        flash('Email exists. Please sign up with a different email.')
    else:
        crud.create_user(email, first_name, last_name, username, password, join_date)
        flash('Account created successfully!')

    return redirect('/')




@app.route('/users/<username>')
def show_user(username):
    """Show details for a user"""
    user = crud.get_user_by_id(username)
    ratings = crud.get_user_ratings(username)

    return render_template("user_details.html", user=user, ratings=ratings)


@app.route("/logout")
def log_out_user():
    """Log out user"""

    if "user_id" in session:
        del session["user_id"]
        flash("Logged out")

    return redirect("/")


# ---------- BOOK ROUTES ---------- #

@app.route('/books')
def show_book_list():
    """Show list of books. 
    If user selected genre: filter by genre.
    Else: If user entered title search, filter by title
    Else: display entire book list.
    """
    
    user_genre = None
    user_title_search = None
    user_author_search = None

    if 'genre' in request.args:
        user_genre = request.args['genre']
        books = helper.get_books_by_genre(user_genre)

    elif 'title_search' in request.args:
        user_title_search = request.args['title_search']
        books = helper.get_books_by_title(user_title_search)

        if books == None:
            flash('No results found')

    elif 'author_search' in request.args:
        user_author_search = request.args['author_search']
        authors = helper.get_books_by_author(user_author_search)

        if books == None:
            flash('No results found')
        
    else: 
        books = crud.get_all_books()

    return render_template("all_books.html", 
                            books=books, 
                            genre=user_genre,
                            authors=authors)


@app.route('/books/<int:book_id>')
def show_book(book_id):
    """Show details for a book."""
    
    author = crud.get_author_name_by_book_id(book_id)
    book = crud.get_book_by_id(book_id)
    location_dict, location_list = helper.get_locations(book_id)

    return render_template("book_details.html", 
                            author=author, 
                            book=book,
                            book_locations=location_dict,
                            location_list=location_list, 
                            MAPS_JS_KEY=MAPS_JS_KEY)


@app.route('/log_book')
def show_log_book_form():

    return render_template("log_book.html")


# ---------- AUTHOR ROUTES ---------- #

@app.route('/authors')
def all_authors():
    """Display all authors."""
    authors = crud.get_all_authors()

    return render_template("all_authors.html", authors=authors)


@app.route('/authors/<int:author_id>')
def show_author(author_id):
    """Show details for an author."""
    
    author = crud.get_author_by_id(author_id)

    return render_template("author_details.html", author=author)


# ---------- LOCATION ROUTES ---------- #

@app.route('/map')
def index_page():
    """View Map."""

    return render_template('map.html', MAPS_JS_KEY=MAPS_JS_KEY)

@app.route('/locations')
def all_locations():
    """Display all locations."""
    locations = crud.get_all_locations()

    return render_template("all_locations.html", locations=locations)


@app.route('/locations/<int:loc_id>')
def show_location(loc_id):
    """Show details for a location."""
    
    location = crud.get_location_by_id(loc_id)

    return render_template("loc_details.html", 
                            location=location, 
                            MAPS_JS_KEY=MAPS_JS_KEY)


# ---------- RATING ROUTES ---------- #


@app.route('/ratings')
def all_ratings():
    """Display all ratings."""
    ratings = crud.get_all_ratings()

    return render_template("all_ratings.html", ratings=ratings)


@app.route('/ratings/<int:rating_id>')
def show_rating(rating_id):
    """Show details for a location."""
    
    rating = crud.get_rating_by_id(rating_id)

    return render_template("rating_details.html", 
                            rating=rating)


# ---------- AJAX / JSON ROUTES ---------- #

@app.route("/user/loggedin")
def is_user_logged_in():
    """Check if user is logged in"""

    if "user_id" in session:
        return "true"

    else:
        return "false"



if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)