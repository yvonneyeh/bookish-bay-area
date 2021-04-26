"""Models for book app."""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
# from wtforms import StringField, TextField, Form
# from wtforms.validators import DataRequired, Length

# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy_searchable import make_searchable
# from sqlalchemy_utils.types import TSVectorType

# app = Flask(__name__)
db = SQLAlchemy()
DATABASE_URL = os.environ['DATABASE_URL']

# ENV = 'prod'

# if ENV == 'dev':
#     app.debug = True
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///books'
# else:
#     app.debug = False
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'DATABASE_URL'

# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


# Base = declarative_base()

# make_searchable()

# classes (User, Book, Rating, Author, BookAuthor, Genre, BookGenre, Location, BookLocation)

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    # TODO: Add nullables after data model is tested
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    password_hash = db.Column(db.String(120))
    join_date = db.Column(db.DateTime)
    bio = db.Column(db.Text)
    website = db.Column(db.String)
    pronouns = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    # Password hashing functions

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User username={self.username} email={self.email}>'


class Book(db.Model):
    """A book."""

    __tablename__ = "books"

    __searchable__ = ['title', 'description', 'pub_date', 'isbn']

    # TODO: ADD NULLABLES , nullable = False to title, author_id, isbn
    book_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'))
    description = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)
    cover_path = db.Column(db.String)
    isbn = db.Column(db.String)
    pages = db.Column(db.Integer)
    link = db.Column(db.String)
    
    # relationships
    # ratings = a list of Rating objects
    # locations = a list of Location objects, with secondary book_loc
   
    # association table relationships
    author_rel = db.relationship(
                                'Author',
                                backref=db.backref('books', order_by=book_id))

    genre_rel = db.relationship('Genre',
                                secondary='book_genre',
                                backref='books')

    def as_dict(self):
        return {'title': self.title}

    def __repr__(self):
        return f'<Book book_id={self.book_id} title={self.title}>'


class Rating(db.Model):
    """A user's saved book - or a rating on a book."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    # username = db.Column(db.String, db.ForeignKey('users.username'))
    log_date = db.Column(db.DateTime)
    score = db.Column(db.Integer)
    read = db.Column(db.Boolean, default=False)

    # book_id, user_id, log_date, score

    # relationships
    user = db.relationship('User', backref='ratings')

    book = db.relationship('Book', backref=db.backref('ratings', order_by=book_id))

    def as_dict(self):
        return {self.book.title : self.score}
        
    def __repr__(self):
        return f'<Rating rating_id={self.rating_id} book_id={self.book_id} score={self.score}>'


class Author(db.Model):
    """An author."""

    __tablename__ = "authors"

    __searchable__ = ['name']

    author_id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return f'<Author author_id={self.author_id} name = {self.name}>'


class BookAuthor(db.Model):
    """A book's author(s)."""

    __tablename__ = "book_author"

    ba_id = db.Column(db.Integer, unique=True, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable = False)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'), nullable = False)

    book_author_rel = db.relationship(
                        'Book',
                        backref=db.backref(
                            'book_author', order_by=author_id))

    author_rel = db.relationship(
                        'Author',
                        backref=db.backref(
                            'book_author', order_by=book_id))

    def __repr__(self):
        return f'<BookAuthor book_id={self.book_id} author_id={self.author_id}>'


class Genre(db.Model):
    """A genre."""

    __tablename__ = "genres"

    genre_id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return f'<Genre genre_id={self.genre_id} name={self.name}>'


class BookGenre(db.Model):
    """A book's genre(s)."""

    __tablename__ = "book_genre"

    bg_id = db.Column(db.Integer, unique=True, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable = False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'), nullable = False)

    genre = db.relationship(
                                'Genre',
                                backref=db.backref('book_genre', order_by=book_id))

    book = db.relationship(
                                'Book',
                                backref=db.backref('book_genre', order_by=book_id))


    def __repr__(self):
        return f'<BookGenre book_id={self.book_id} genre_id={self.genre_id}>'


class Location(db.Model):
    """A location."""

    __tablename__ = "locations"

    __searchable__ = ['name']

    loc_id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)
    address = db.Column(db.String)
    city = db.Column(db.String)
    state = db.Column(db.String)
    description = db.Column(db.String)

    # book = db.relationship('Book', backref='locations')

    # book = db.relationship('Post', backref='author',
    #                     primaryjoin="User.id == Location.user_id")
    # book = db.relationship('Book', backref='locations', )
    # user = db.relationship('User', backref='locations')

    def __repr__(self):
        return f'<Location loc_id={self.loc_id} name={self.name}>'


class BookLocation(db.Model):
    """A book's location(s)."""

    __tablename__ = "book_loc"

    bl_id = db.Column(db.Integer, unique=True, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable = False)
    loc_id = db.Column(db.Integer, db.ForeignKey('locations.loc_id'), nullable = False)


    location = db.relationship(
                                'Location',
                                backref=db.backref('book_loc', order_by=book_id))

    book = db.relationship(
                                'Book',
                                backref=db.backref('book_loc', order_by=book_id))

    # book_loc_rel = db.relationship('Book',
    #                             backref=db.backref(
    #                             'locations'))

    # book = db.relationship('Book', backref='book_loc')
    # location = db.relationship('Location', backref='book_loc')


    # book_location_rel = db.relationship(
    #                     'Book',
    #                     backref=db.backref(
    #                         'locations', order_by=loc_id))

    # book_loc_rel = db.relationship(
    #                     'Book',
    #                     backref=db.backref(
    #                         'book_loc', order_by=loc_id))

    # loc_rel = db.relationship(
    #                     'Location',
    #                     backref=db.backref(
    #                         'book_loc', order_by=book_id))


    def __repr__(self):
        return f'<BookLocation book_id={self.book_id} loc_id={self.loc_id}>'


# class BookSearchForm(Form): 
#     title = StringField('Title', validators=[DataRequired(),Length(max=50)],render_kw={"placeholder": "Book Title"})


# class LocSearchForm(Form): 
#     location = StringField('Location', validators=[DataRequired(),Length(max=50)],render_kw={"placeholder": "Location Name"})

# wa.whoosh_index(app, Book, Author, Location)

##################################################


# def connect_to_db(app):
def connect_to_db(app, db_uri=os.environ.get('DATABASE_URL') or 'postgresql:///books', echo=True):
    print("db_uri on model.py:", os.environ.get('DATABASE_URL') or 'postgresql:///books')
    """Connect the database to our Flask app."""

    ENV = 'prod'

    if ENV == 'dev':
        app.debug = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///books'
    else:
        app.debug = False
        app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    # app.debug = False
    # app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # True for Dev, False when Prod
    # app.config['DEBUG'] = True # Debug mode, remove when done
    # app.config['WHOOSH_BASE'] = 'whoosh'
    # db.app = app
    db.init_app(app)




if __name__ == '__main__':
    from server import app

    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
    connect_to_db(app)
    print('Connected to db!')
