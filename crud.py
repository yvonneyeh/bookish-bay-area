"""CRUD operations."""

from model import *

# USERS
def create_user(email, first_name, last_name, username, password, join_date):
    """Create and return a new user."""

    user = User(email=email, first_name=first_name, last_name=last_name, username=username, password=password, join_date=join_date)

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


# AUTHORS
def create_author(name):
    """Create and return a new user."""

    author = Author(name=name)

    db.session.add(author)
    db.session.commit()

    return author


def get_all_authors():
    """Return all authors."""

    return Author.query.all()


def get_author_by_id(author_id):
    """Return authors given their ID"""

    return Author.query.filter(Author.author_id == author_id).one() 


def get_author_by_name(name):
    """Return authors given their name"""

    return Author.query.filter(Author.name == name).first() 

def get_author_id_by_name(name):
    """Return author's ID given their name"""

    return db.session.query(Author.author_id).filter(Author.name == name).first()
    # return select([Author.author_id]).where(Author.name == name)
    

def get_author_name_by_book_id(id):
    """Return author's name given the ID of a book they wrote"""

    # return db.session.query(Author).filter(Book.book_id == id).first()

    return db.session.query(Author).join(Book, Book.author_id == Author.author_id).first()
    

# BOOKS
def create_book(title, author_id, description, cover_path):
    """Create and return a new book."""

    book = Book(
                title = title, 
                author_id = author_id, 
                description = description, 
                # location = location,
                # pub_date = pub_date, 
                cover_path = cover_path 
                # , isbn = isbn
                # , pages = pages
            )
        
    db.session.add(book)
    db.session.commit()

    return book


def get_all_books():
    """Return all books, sorted alphabetically"""

    # return Book.query.all()
    return Book.query.order_by(Book.title).all()


def get_book_by_id(book_id):
    """Return books given its ID"""

    return Book.query.filter(Book.book_id == book_id).first() 


def get_books_by_title(user_title_search):
    """ Get books based on title search string. 
    """

    books = Book.query.filter(Book.title.like("%" + user_title_search + "%"))\
        .order_by(Book.title)\
        .all()

    return books

def get_books_by_genre(user_genre):
    """ Get subset of books based on genre. 
        Accepts genre entered by user, returns books.

    """
    if user_genre == 'All':
        books = Book.query.order_by(Book.title).all()
    else:
        books = Book.query.filter(Book.book.like("%" + user_genre + "%"))\
            .order_by(Book.title)\
            .all()

    return movies

# GENRES
def create_genre(name):
    """Create and return a new book."""

    genre = Genre(name = name)
        
    db.session.add(genre)
    db.session.commit()

    return genre

def get_all_genres():
    """Return all genres."""

    return Genre.query.all()


def get_genre_by_name(name):
    """Return genre given its name"""

    return Genre.query.filter(Genre.name == name).first() 


# LOCATIONS
def create_location(name, lat, lng):
    """Create and return a new location."""

    location = Location(name = name, 
                        lat = lat, 
                        lng = lng)
        
    db.session.add(location)
    db.session.commit()

    return location

def get_all_locations():
    """Return all locations."""

    return Location.query.order_by(Location.name).all()


def get_location_by_name(name):
    """Return location given its name"""

    return Location.query.filter(Location.name == name).first() 


def get_location_by_id(loc_id):
    """Return location given its ID"""

    return Location.query.filter(Location.loc_id == loc_id).one() 


def get_location_id_by_name(name):
    """Return location's ID given their name"""

    return db.session.query(Location.loc_id).filter(Location.name == name).first()


# RATINGS
def create_rating(user, book, score):
    """Create and return a new book rating."""

    rating = Rating(user=user, book=book, score=score)
    
    db.session.add(rating)
    db.session.commit()

    return rating


if __name__ == '__main__':
    from server import app
    connect_to_db(app)