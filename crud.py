"""CRUD operations."""

from model import *


def create_user(email, password):
    """Create and return a new user."""

    user = User(email=email, password=password)

    db.session.add(user)
    db.session.commit()

    return user


def get_all_users():
    """Return all users."""

    return User.query.all()


def get_user_by_email(email):
    """Return a user given an email address."""

    return User.query.filter(User.email == email).first()


def get_user_by_id(username):
    """Return user given their ID"""

    return User.query.filter(User.username == username).one() 


def create_author(name):
    """Create and return a new user."""

    author = Author(name=name)

    db.session.add(author)
    db.session.commit()

    return author

def create_book(title, author_id, description, pub_date, cover_path, isbn):
    """Create and return a new book."""

    book = Book(
                title = title, 
                author_id = author_id, 
                description = description, 
                pub_date = pub_date, 
                cover_path = cover_path, 
                isbn = isbn
                # , 
                # pages = pages
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


def create_rating(user, book, score):
    """Create and return a new book rating."""

    rating = Rating(user=user, book=book, score=score)
    
    db.session.add(rating)
    db.session.commit()

    return rating


if __name__ == '__main__':
    from server import app
    connect_to_db(app)