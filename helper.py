"""Helper functions for server.py"""

from model import *

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
    
    
# TODO: fix author search
def get_author_books_by_search(user_author_search):
    """ Get author's books based on author name search string. 
    """

    authors = Author.query.filter(Author.nane.like("%" + user_author_search + "%"))\
        .join(Book, Book.author_id == Author.author_id)\
        .order_by(Book.title)\
        .all()

    return authors

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

    locations = Location.query.filter_by(book_id=book_id).all()

    location_dict = {}
    location_list = [] 

    for location in locations:
        dict_key = str(location.lat) + str(location.lng)

        if location.latitude == 37.786220 and location.longitude == -122.432210:
            location_list.append(location.location_description)

        # elif dict_key in location_dict: 
        #     location_dict[dict_key]['desc'] += "; <p>" + location.location_description

        else:

            location_dict[dict_key] = {}
            location_dict[dict_key]['lat'] = location.latitude
            location_dict[dict_key]['lng'] = location.longitude
            location_dict[dict_key]['name'] = location.name

    return location_dict, location_list