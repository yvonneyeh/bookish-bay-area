"""Server for Bookish Bay Area app."""

from flask import Flask, render_template, request, flash, session, redirect, jsonify
from model import connect_to_db, Book
from sqlalchemy_searchable import search
from random import randint
import faker
import crud
import helper

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


@app.route('/map')
def index_page():
    """View Map."""

    return render_template('map.html')


@app.route('/login')
def login():
    """View Login page."""

    return render_template('login.html')

# @app.route('/books')
# def all_books():
#     """Display all books."""
#     books = crud.get_all_books()

#     return render_template("all_books.html", books=books)


@app.route('/books')
def movie_list():
    """Show list of books. 
    If user selected genre: filter by genre.
    Else: If user entered title search, filter by title
    Else: display entire book list.
    """
    
    user_genre = None
    user_title_search = None

    if 'genre' in request.args:
        user_genre = request.args['genre']
        books = helper.get_books_by_genre(user_genre)

    elif 'title_search' in request.args:
        user_title_search = request.args['title_search']
        books = helper.get_books_by_title(user_title_search)
        
    else: 
        books = crud.get_all_books()

    return render_template("all_books.html", 
                            books=books, 
                            genre=user_genre)


@app.route('/books/<int:book_id>')
def show_book(book_id):
    """Show details for a book."""
    
    author = crud.get_author_name_by_book_id(book_id)
    book = crud.get_book_by_id(book_id)
    # location_dict, location_list = crud.get_locations(book_id)

    return render_template("book_details.html", 
                            author=author, 
                            book=book)
                            # book_locations=location_dict,
                            # location_list=location_list)


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



@app.route('/locations')
def all_locations():
    """Display all locations."""
    locations = crud.get_all_locations()

    return render_template("all_locations.html", locations=locations)


@app.route('/locations/<int:loc_id>')
def show_location(loc_id):
    """Show details for a location."""
    
    location = crud.get_location_by_id(loc_id)

    return render_template("loc_details.html", location=location)


@app.route('/users')
def all_users():
    """Display all users."""
    users = crud.get_all_users()

    return render_template("all_users.html", users=users)


@app.route('/users', methods=['POST'])
def create_account():
    """Create a new user account."""

    password = request.form.get('password')
    email = request.form.get('email')

    if crud.get_user_by_email(email) != None:
        flash('Email exists. Please sign up with a different email.')
    else:
        crud.create_user(email, password)
        flash('Account created successfully!')

    return redirect('/')


@app.route('/login', methods=['POST'])
def log_in_user():
    """Login user and redirect to homepage."""

    username = request.form.get('username')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')

    user_object = crud.get_user_by_email(email)

    if user_object != None:
        if password == user_object.password != None:
            session['username'] = user_object.username
            # print('Logged in!')
            flash('Logged in!')
        else:
            flash('Incorrect password')   
    else:
        flash('Email does not exist. Please sign up above.')
    
    return redirect('/')


@app.route('/users/<username>')
def show_user(username):
    """Show details for a user"""
    user = crud.get_user_by_id(username)

    return render_template("user_details.html", user=user)


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)