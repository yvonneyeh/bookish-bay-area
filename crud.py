"""CRUD operations."""

from model import *


def create_reader(email, password):
    """Create and return a new reader."""

    reader = Reader(email=email, password=password)

    db.session.add(reader)
    db.session.commit()

    return reader


def get_all_readers():
    """Return all readers."""

    return Reader.query.all()


def get_reader_by_email(email):
    """Return a reader given an email address."""

    return Reader.query.filter(Reader.email == email).first()


def get_reader_by_id(user_id):
    """Return reader given their ID"""

    return Reader.query.filter(Reader.user_id == user_id).one() 


def create_author(name):
    """Create and return a new reader."""

    author = Author(name=name)

    db.session.add(author)
    db.session.commit()

    return author

def create_book(title, author_id, description, pub_date, cover_path, isbn, pages):
    """Create and return a new book."""

    book = Book(
                title = title, 
                author_id = author_id, 
                description = description, 
                pub_date = pub_date, 
                cover_path = cover_path, 
                isbn = isbn, 
                pages = pages
            )
        
    db.session.add(book)
    db.session.commit()

    return book


def get_all_books():
    """Return all books"""

    return Book.query.all()


def get_book_by_id(book_id):
    """Return books given its ID"""

    return Book.query.filter(book.book_id == book_id).one() 


def create_rating(reader, book, score):
    """Create and return a new book rating."""

    rating = Rating(reader=reader, book=book, score=score)
    
    db.session.add(rating)
    db.session.commit()

    return rating


if __name__ == '__main__':
    from server import app
    connect_to_db(app)