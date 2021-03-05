"""Helper functions for server.py"""
# from model import *
from crud import *
from sqlalchemy import and_, or_, not_
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="app")


def create_user_submitted_loc(name, address):
    """Create and return a new user-submitted location."""

    location = geolocator.geocode(address)
    lat = location.latitude
    lng = location.longitude

    location = create_location(name, lat, lng, address)
        
    db.session.add(location)
    db.session.commit()

    return location


def get_books_by_search(user_search):
    """ Get books based on search string. """

    books = Book.query.filter(or_(Book.title.ilike("%" + user_search + "%")),
                                (Author.name.ilike("%" + user_search + "%")))\
        .order_by(Book.title)\
        .all()

    return books


def get_books_by_title(user_title_search):
    """ Get books based on title search string. 
    """

    books = Book.query.filter(Book.title.ilike("%" + user_title_search + "%"))\
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
        books = Book.query.filter(Book.genre_rel.ilike("%" + user_genre + "%"))\
            .order_by(Book.title)\
            .all()

    return books
    
    
def get_books_by_author(user_author_search):
    """ Get author's books based on author name search string. 
    """

    books = db.session.query(Book).filter(Author.name.ilike("%" + user_author_search + "%"))\
            .join(Author, Book.author_id == Author.author_id)\
            .order_by(Book.title)\
            .all()

    return books


def get_users_rated_books(user_id):
    """Query database to find Ratings objects belonging to user
        & not marked 'read."""

    read_books = Rating.query.filter((Rating.user_id == user_id)
                                    & (Rating.read.is_(True))).all()

    return read_books


def get_users_saved_book(user_id, book_id):
    """Query database to find Ratings objects belonging to user
        & matching book_id"""

    saved_book = Rating.query.filter((Rating.user_id == user_id)
                                              & (Rating.book_id == book_id)).first()

    return saved_book


def get_session_users_saved_book(user_id, book_id):
    """Query database to find Ratings objects belonging to user in session
        & matching book_id"""

    saved_book = Rating.query.filter((Rating.user_id == session["user_id"])
                                              & (Rating.book_id == book_id)).first()

    return saved_book

def get_rating_by_ids(user_id, book_id):
    """Query database to find Ratings objects matching search params."""

    rating = Rating.query.filter((Rating.user_id == user_id) 
                                & (Rating.book_id == book_id)).first()

    return rating


def get_all_locations():

    locations = db.session.query(BookLocation).all()

    location_dict = {}
    location_list = [] 

    for loc in locations:
        dict_key = str(loc.location.lat) + str(loc.location.lng)

        if loc.location.lat == 37.786220 and loc.location.lng == -122.432210:
            location_list.append(loc.location.name)

        elif dict_key in location_dict: 
            location_dict[dict_key]['desc'] = loc.location.description

        else:

            location_dict[dict_key] = {}
            location_dict[dict_key]['lat'] = loc.location.lat
            location_dict[dict_key]['lng'] = loc.location.lng
            location_dict[dict_key]['name'] = loc.location.name

    return location_dict, location_list


# TODO: FIX query - user - ratings - books - book_loc
def get_booklocs_by_user(user_id):
    """ Retrieve book locations
    """

    # locations = FIX THIS, join
    locations = db.session.query(BookLocation).filter_by(user_id=user_id).all() # this is a list
    print(locations)

    location_dict = {}
    location_list = [] 

    for loc in locations:
        dict_key = str(loc.location.lat) + str(loc.location.lng)

        if loc.location.lat == 37.786220 and loc.location.lng == -122.432210:
            location_list.append(loc.location.name)

        elif dict_key in location_dict: 
            location_dict[dict_key]['desc'] = loc.location.description

        else:

            location_dict[dict_key] = {}
            location_dict[dict_key]['lat'] = loc.location.lat
            location_dict[dict_key]['lng'] = loc.location.lng
            location_dict[dict_key]['name'] = loc.location.name

    return location_dict, location_list


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

    locations = db.session.query(BookLocation).filter_by(book_id=book_id).all() # this is a list
    print(locations)

    location_dict = {}
    location_list = [] 

    for loc in locations:
        dict_key = str(loc.location.lat) + str(loc.location.lng)

        if loc.location.lat == 37.786220 and loc.location.lng == -122.432210:
            location_list.append(loc.location.name)

        elif dict_key in location_dict: 
            location_dict[dict_key]['desc'] = loc.location.description

        else:

            location_dict[dict_key] = {}
            location_dict[dict_key]['lat'] = loc.location.lat
            location_dict[dict_key]['lng'] = loc.location.lng
            location_dict[dict_key]['name'] = loc.location.name

    return location_dict, location_list