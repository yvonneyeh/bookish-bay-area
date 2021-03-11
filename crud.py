"""CRUD operations."""

from model import *

# USERS
def create_user(email, first_name, last_name, username, password, join_date, website, city, pronouns):
    """Create and return a new user."""

    user = User(email=email, first_name=first_name, last_name=last_name, username=username, password=password, join_date=join_date, website=website, city=city, pronouns=pronouns)

    db.session.add(user)
    db.session.commit()

    return user


def get_all_users():
    """Return all users."""

    return User.query.all()


def get_user_by_email(email):
    """Return a user given an email address."""

    return User.query.filter(User.email == email).first()

    
def get_user_by_username(username):
    """Return user given their username"""

    return User.query.filter(User.username == username).first() 

def get_user_by_id(user_id):
    """Return user given their ID"""

    return User.query.filter(User.user_id == user_id).first() 

def get_user_by_email_id(email, username):

    return User.query.filter((User.email == email) |
                             (User.username == username)).all()


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

# # TODO: fix author search
# def get_author_books_by_search(user_author_search):
#     """ Get author's books based on author name search string. 
#     """

#     authors = Author.query.filter(Author.nane.like("%" + user_author_search + "%"))\
#         .join(Book, Book.author_id == Author.author_id)\
#         .order_by(Book.title)\
#         .all()

#     return authors

def get_author_id_by_name(name):
    """Return author's ID given their name"""

    return db.session.query(Author.author_id).filter(Author.name == name).first()
    

def get_author_name_by_book_id(id):
    """Return author's name given the ID of a book they wrote"""

    # return db.session.query(Author).filter(Book.book_id == id).first()

    return db.session.query(Author).join(Book, Book.author_id == Author.author_id).first()
    

# BOOKS
def create_book(title, author_id, description, cover_path, isbn, link):
    """Create and return a new book."""

    book = Book(
                title = title, 
                author_id = author_id, 
                description = description, 
                # location = location,
                # pub_date = pub_date, 
                cover_path = cover_path,
                isbn = isbn,
                link = link
                # , pages = pages
            )
        
    db.session.add(book)
    db.session.commit()

    return book


def get_all_books():
    """Return all books, sorted alphabetically"""

    # return Book.query.all()
    return Book.query.order_by(Book.title).all()


# def get_all_book_titles():
#     """Return all book titles, sorted alphabetically"""

#     return Book.query(Book.title).order_by(Book.title).all()


def get_book_by_id(book_id):
    """Return books given its ID"""

    return Book.query.filter(Book.book_id == book_id).first() 


def get_book_by_title(title):
    """Return books given its title"""

    return Book.query.filter(Book.title == title).first() 


def get_book_id_by_title(title):
    """Return book's ID given its title"""

    return db.session.query(Book.book_id).filter(Book.title == title).first()


def get_books_by_author_by(author_id):
    """Return all books by an author given the author's ID"""

    return Book.query.filter(Book.author_id == author_id).all() 

# GENRES
def create_genre(name):
    """Create and return a new book."""

    genre = Genre(name = name)
        
    db.session.add(genre)
    db.session.commit()

    return genre


def create_book_genres(book_id, genre_id):
    """Create and return a new book genre."""

    book_genre = BookGenre(book_id = book_id, genre_id = genre_id)

    db.session.add(book_genre)
    db.session.commit()

    return book_genre



def get_all_genres():
    """Return all genres."""

    return Genre.query.all()


def get_genre_by_name(name):
    """Return genre given its name"""

    return Genre.query.filter(Genre.name == name).first() 


def get_genre_by_id(genre_id):
    """Return authors given their ID"""

    return Genre.query.filter(Genre.genre_id == genre_id).one() 


# LOCATIONS
def create_book_location(book_id, loc_id):
    """Create and return a new book location."""

    book_loc = BookLocation(book_id = book_id, loc_id = loc_id)

    db.session.add(book_loc)
    db.session.commit()

    return book_loc


def create_location(name, lat, lng, address):
    """Create and return a new location."""

    location = Location(name = name, 
                        lat = lat, 
                        lng = lng,
                        address = address)
        
    db.session.add(location)
    db.session.commit()

    return location


def get_all_locations():
    """Return all locations."""

    return Location.query.order_by(Location.name).all()


# def get_all_loc_names():
#     """Return all location names, sorted alphabetically"""

#     return Location.query(Location.name).order_by(Location.name).all()


def get_all_book_locations(book_id):
    """Return all book locations."""
    return BookLocation.query.filter(BookLocation.book_id == book_id).all()


def get_location_by_name(name):
    """Return location given its name"""

    return Location.query.filter(Location.name == name).first() 


def get_location_by_id(loc_id):
    """Return location given its ID"""

    return Location.query.filter(Location.loc_id == loc_id).one() 


def get_location_id_by_name(name):
    """Return location's ID given their name"""

    return db.session.query(Location.loc_id).filter(Location.name == name).first()


def get_locations(book_id):
    """ Retrieve book locations
        Accepts book ID, returns locations formatted into 2 structures:

        1. Location dictionary for locations with meaningful latitude & longitude
        2. Location list for locations for which the Google maps API could not
           identify a specific location from the description. For these locations, 
           the Google maps API returns coordinates for Hackbright in San Francisco.
           Load these locations into a list, to display without markers on the book
           detail page, because the markers would be misleading.
    """

    locations = db.session.query(BookLocation).filter_by(book_id=book_id).all()
    print(locations)

# def get_locations(book_id):
#     """ Retrieve book locations
#         Accepts book ID, returns locations formatted into 2 structures:

#         1. Location dictionary for locations with meaningful latitude & longitude
#         2. Location list for locations for which the Google maps API could not
#            identify a specific location from the description. For these locations, 
#            the Google maps API returns coordinates for Hackbright in San Francisco.
#            Load these locations into a list, to display without markers on the book
#            detail page, because the markers would be misleading.
#     """

#     locations = Location.query.filter_by(book_id=book_id).all()

#     location_dict = {}
#     location_list = [] 

#     for location in locations:
#         dict_key = str(location.lat) + str(location.lng)

#         if location.latitude == 37.786220 and location.longitude == -122.432210:
#             location_list.append(location.location_description)

#         # elif dict_key in location_dict: 
#         #     location_dict[dict_key]['desc'] += "; <p>" + location.location_description

#         else:

#             location_dict[dict_key] = {}
#             location_dict[dict_key]['lat'] = location.latitude
#             location_dict[dict_key]['lng'] = location.longitude
#             location_dict[dict_key]['name'] = location.name

#     return location_dict, location_list


# RATINGS
def create_rating(user_id, book_id, log_date, score, read):
    """Create and return a new book rating."""


    rating = Rating(user_id=user_id, book_id=book_id, log_date=log_date, score=score, read=read)
    
    db.session.add(rating)
    db.session.commit()

    return rating


def get_all_ratings():
    """Return all ratings."""

    return Rating.query.all()


def get_all_ratings_order_by_new():
    """Return all ratings order by most recently rated."""

    return Rating.query.order_by(Rating.rating_id.desc()).all()


def get_rating_by_id(rating_id):
    """Return rating given its ID"""

    return Rating.query.filter(Rating.rating_id == rating_id).one() 


def get_user_ratings(username):
    """Get user's saved book ratings."""

    ratings = db.session.query(Rating).join(User, Rating.user_id == User.user_id)\
                .filter((User.username == username)).all()


    return ratings


if __name__ == '__main__':
    from server import app
    connect_to_db(app)