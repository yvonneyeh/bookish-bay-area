"""Helper functions for server.py"""
# from model import *
import os
from crud import *
from sqlalchemy import and_, or_, not_
from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="app")

MAPS_GEOCODING_KEY = os.environ['MAPS_GEOCODING_KEY']

def call_geocoding_api(search_terms):
    """Query Google Maps Geocoding API to convert search terms to
    lat/lng coordinates"""

    api_url = "https://maps.googleapis.com/maps/api/geocode/json"
    payload = {
        "address": search_terms,
        "key": MAPS_GEOCODING_KEY
    }

    r = requests.get(api_url, params=payload)
    response = r.json()

    # Check to see if search was valid
    if response.get("results"):
        lat_long = response["results"][0]["geometry"]["location"]
        return lat_long

    # Return error message if message invalid
    else:
        return "Invalid search terms"


def create_user_submitted_loc(name, address, city, state):
    """Create and return a new user-submitted location."""

    location = geolocator.geocode(address)
    lat = location.latitude
    lng = location.longitude

    location = create_location(name, lat, lng, address, city, state)
        
    db.session.add(location)
    db.session.commit()

    return location


# def create_user_submitted_bookloc(book_id, loc_id):
#     """Create and return a new user-submitted location."""

#     bookloc = create_book_location(book_id, loc_id)
        
#     db.session.add(bookloc)
#     db.session.commit()

#     return location


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

    saved_book = Rating.query.filter((Rating.user_id == user_id)
                                              & (Rating.book_id == book_id)).first()

    return saved_book

def get_rating_by_ids(user_id, book_id):
    """Query database to find Ratings objects matching search params."""

    rating = Rating.query.filter((Rating.user_id == user_id) 
                                & (Rating.book_id == book_id)).first()

    return rating


def get_locations_by_search(user_loc_search):
    """ Get books based on location search string. 
    """

    locations = Location.query.filter(Location.name.ilike("%" + user_loc_search + "%"))\
                .order_by(Location.name)\
                .all()

    return locations


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
            location_dict[dict_key]['id'] = loc.location.loc_id
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


def get_books_by_location(loc_id):
    """ Retrieve book locations
        Accepts book ID, returns locations formatted into 2 structures:

        1. Location dictionary for locations with meaningful latitude & longitude
        2. Location list for locations for which the Google maps API could not
           identify a specific location from the description. For these locations, 
           the Google maps API returns coordinates for Hackbright in San Francisco.
           Load these locations into a list, to display without markers on the book
           detail page, because the markers would be misleading.
    """

    books = db.session.query(BookLocation).filter_by(loc_id=loc_id).all() # this is a list
    print(books)

    book_dict = {}
    book_list = [] 

    for loc in books:
        dict_key = loc.book.book_id
        print(dict_key)

        book_list.append(loc.book.title)

        # TODO: FIX BOOK DICTIONARY
        if dict_key not in book_dict: 
            book_dict.get('dict_key',{})

        else:

            book_dict[dict_key] = {}
            book_dict[dict_key]['title'] = loc.book.title
            book_dict[dict_key]['link'] = "/books/<int:loc.book.book_id>"
            book_dict[dict_key]['cover'] = loc.book.cover_path

    print(book_list)
    print(book_dict)

    return book_dict, book_list


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

        # if loc.location.lat == 37.786220 and loc.location.lng == -122.432210:
        location_list.append(loc.location.name)

        if dict_key in location_dict: 
            location_dict[dict_key]['desc'] = loc.location.description

        else:

            location_dict[dict_key] = {}
            location_dict[dict_key]['lat'] = loc.location.lat
            location_dict[dict_key]['lng'] = loc.location.lng
            location_dict[dict_key]['name'] = loc.location.name

    return location_dict, location_list