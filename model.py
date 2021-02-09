"""Models for book app."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Reader(db.Model):
    """A user."""

    __tablename__ = "readers"

    user_id = db.Column(db.Integer, unique=True, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    join_date = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Reader user_id={self.user_id} email={self.email}>'



class Book(db.Model):
    """A book."""

    __tablename__ = "books"

    book_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String)
    author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'), nullable = False)
    description = db.Column(db.Text)
    release_date = db.Column(db.DateTime)
    cover_path = db.Column(db.String)

    # ratings = a list of Rating objects

    def __repr__(self):
        return f'<Book book_id={self.book_id} title={self.title}>'


class Rating(db.Model):
    """A rating."""

    __tablename__ = "ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    score = db.Column(db.Integer)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'))
    log_date = db.Column(db.DateTime)

    book = db.relationship('Book', backref='ratings')
    user = db.relationship('User', backref='ratings')

    def __repr__(self):
        return f'<Rating rating_id={self.rating_id} score={self.score}>'


class Author(db.Model):
    """An author."""

    __tablename__ = "authors"

    author_id = db.Column(db.Integer, unique=True, primary_key=True)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    dob = db.Column(db.DateTime)

    def __repr__(self):
        return f'<Author author_id={self.author_id} Name = {self.first_name} {self.last_name}>'


class Genre(db.Model):
    """A genre."""

    __tablename__ = "genres"

    genre_id = db.Column(db.Integer, unique=True, primary_key=True)
    name = db.Column(db.String)

    def __repr__(self):
        return f'<Genre genre_id={self.genre_id} Name={self.name}>'


class BookGenre(db.Model):
    """A book's genre(s)."""

    __tablename__ = "book_genres"

    bg_id = db.Column(db.Integer, unique=True, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'), nullable = False)
    genre_id = db.Column(db.Integer, db.ForeignKey('genre.author_id'), nullable = False)


    def __repr__(self):
        return f'<BookGenre book_id={self.book_id} genre_id={self.genre_id}>'