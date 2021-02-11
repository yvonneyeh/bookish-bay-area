"""Server for Bookish Bay Area app."""

from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import connect_to_db, Book
from random import randint
import crud

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


@app.route('/books')
def all_books():
    """Display all books."""
    books = crud.get_all_books()

    return render_template("all_books.html", books=books)


@app.route('/books/<int:book_id>')
def show_book(book_id):
    """Show details for a book."""
    
    book = crud.get_book_by_id(book_id)

    return render_template("book_details.html", book=book)


@app.route('/readers')
def all_readers():
    """Display all readers."""
    reader = crud.get_all_readers()

    return render_template("all_readers.html", reader=readers)


@app.route('/readers', methods=['POST'])
def create_account():
    """Create a new user account."""

    password = request.form.get('password')
    email = request.form.get('email')

    if crud.get_reader_by_email(email) != None:
        flash('Email exists. Please sign up with a different email.')
    else:
        crud.create_reader(email, password)
        flash('Account created successfully!')

    return redirect('/')


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)