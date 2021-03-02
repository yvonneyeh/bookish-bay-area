"""Helper functions for server.py"""

from model import *

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
        & not marked complete."""

    read_books = Rating.query.filter((Rating.user_id == user_id)
                                    & (Rating.read.is_(True))).all()

    return read_books


def get_rating_by_ids(user_id, book_id):
    """Query database to find Ratings objects matching search params."""

    rating = Rating.query.filter((Rating.user_id == user_id) 
                                & (Rating.book_id == book_id)).first()

    return rating




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
        # dict_key = str(location.books.lat) + str(location.books.lng)

        if loc.location.lat == 37.786220 and loc.location.lng == -122.432210:
            location_list.append(location.location_description)

        elif dict_key in location_dict: 
            location_dict[dict_key]['desc'] += "; <p>" + location.location_description

        else:

            location_dict[dict_key] = {}
            location_dict[dict_key]['lat'] = loc.location.lat
            location_dict[dict_key]['lng'] = loc.location.lng
            location_dict[dict_key]['name'] = loc.location.name

    return location_dict, location_list