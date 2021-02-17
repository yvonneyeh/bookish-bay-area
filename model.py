"""Models for book app."""

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

app = Flask(__name__)

class User(db.Model):
    """A user."""

    __tablename__ = "users"

    # TODO: Add nullables after data model is tested
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    username = db.Column(db.String, unique=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    join_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<User username={self.username} email={self.email}>'


class Book(db.Model):
    """A book."""

    __tablename__ = "books"

    # TODO: ADD NULLABLES , nullable = False to title, author_id, isbn
    book_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'))
    description = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)
    cover_path = db.Column(db.String)
    isbn = db.Column(db.String)
    pages = db.Column(db.Integer)
    
    # relationships
    # ratings = a list of Rating objects
   
    # association table relationships
    author_rel = db.relationship(
                                'Author',
                                backref=db.backref('books', order_by=book_id))

    # genre_rel = db.relationship(
    #                             'Genre',
    #                             backref=db.backref('books', order_by=book_id))

    genre_rel = db.relationship('Genre',
                                secondary='book_genre',
                                backref='books')

    loc_rel = db.relationship('Location',
                                secondary='book_loc',
                                backref='books')

    def __repr__(self):
        return f'<Book book_id={self.book_id} title={self.title}>'


class Rating(db.Model):
    """A rating."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    username = db.Column(db.String, db.ForeignKey('users.username'))
    log_date = db.Column(db.DateTime)
    score = db.Column(db.Integer)

    # relationships
    book = db.relationship('Book', backref='ratings')
    user = db.relationship('User', backref='ratings')

    def __repr__(self):
        return f'<Rating rating_id={self.rating_id} score={self.score}>'


class Author(db.Model):
    """An author."""

    __tablename__ = "authors"

    author_id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return f'<Author author_id={self.author_id} Name = {self.name}>'


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
        return f'<Genre genre_id={self.genre_id} Name={self.name}>'


class BookGenre(db.Model):
    """A book's genre(s)."""

    __tablename__ = "book_genre"

    bg_id = db.Column(db.Integer, unique=True, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable = False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genres.genre_id'), nullable = False)


    def __repr__(self):
        return f'<BookGenre book_id={self.book_id} genre_id={self.genre_id}>'


class Location(db.Model):
    """A location."""

    __tablename__ = "locations"

    loc_id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String)
    lat = db.Column(db.Float)
    lng = db.Column(db.Float)

    def __repr__(self):
        return f'<Location loc_id={self.loc_id} Name={self.name}>'


class BookLocation(db.Model):
    """A book's genre(s)."""

    __tablename__ = "book_loc"

    bl_id = db.Column(db.Integer, unique=True, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable = False)
    loc_id = db.Column(db.Integer, db.ForeignKey('locations.loc_id'), nullable = False)

    # book_loc_rel = db.relationship('Book',
    #                 backref=db.backref(
    #                 'locations', order_by=loc_id))

    def __repr__(self):
        return f'<BookLocation book_id={self.book_id} loc_id={self.loc_id}>'



##################################################


def connect_to_db(app):
    """Connect the database to our Flask app."""

    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres:///books'
    app.config['SQLALCHEMY_ECHO'] = False
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)


if __name__ == '__main__':
    from server import app

    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.
    connect_to_db(app)
    print('Connected to db!')
