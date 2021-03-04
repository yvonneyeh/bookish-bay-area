"""Script to seed database."""

import os
from random import choice, randint, getrandbits
from datetime import date, datetime
from faker import Faker
from geopy.geocoders import Nominatim
import csv

import crud
import model
import server

os.system('dropdb books')
os.system('createdb books')

fake = Faker()

# # f = open('data/silicon_valley_books.csv')
# f = open('data/small.csv')
# # csv_f = csv.reader(f)
# f1 = open('data/test_book_data.csv')
# f2 = open('data/silicon_valley_books.csv')

users_in_db = []
def seed_users():
    first_name = 'Yvonne'
    last_name = 'Yeh'
    username = 'yvonneyeh'
    password = 'test'
    password_hash = 'test'
    join_date = '2020-03-17'
    email = 'code@yvonneyeh.com'
    yy = crud.create_user(email, first_name, last_name, username, password, join_date)
    users_in_db.append(yy)

    for n in range(20):
        email = f'reader{n}@books.book'
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f'{first_name}{last_name}'
        password_hash = 'test'
        join_date = datetime.today()
        new_user = crud.create_user(email, first_name, last_name, username, password_hash, join_date)
        users_in_db.append(new_user)
    print(users_in_db)

ratings_in_db = []
def seed_ratings():
    for n in range(100):
        user_id = randint(1,10)
        book_id = randint(1,80)
        log_date = datetime.today()
        score = randint(1,5)
        read = bool(getrandbits(1)) #choice([True, False])
        rate_obj = crud.create_rating(user_id, book_id, log_date, score, read)  
        ratings_in_db.append(rate_obj)
    print(ratings_in_db)

genres_in_db = []
def seed_genres(filename):
    """Add new genres to Genre table."""

    opened_file = open(filename)
    
    for name in opened_file:
        if crud.get_genre_by_name(name) == None:
            genre_obj = crud.create_genre(name)
            genres_in_db.append(genre_obj)
    print(genres_in_db)


authors_in_db = []
def seed_authors(filename):
    f1 = open(filename)
    csv_f = csv.reader(f1)
    for row in csv_f:
        author, link_href, title, author, description, genres, isbn, location, cover, date = row
        # web_scraper_order, web_scraper_start_url, link, link_href, title, author, description, genres, isbn, location, cover, date = row
        # print(crud.get_author_by_name(author))
        if crud.get_author_by_name(author) == None:
        # print(author)
        # else:
            author_obj = crud.create_author(author)
            authors_in_db.append(author_obj)
    print(authors_in_db)


locs_in_db = []

def seed_addresses(filename):
    """Add new sample addresses to Location table."""

    f = open(filename)
    csv_f = csv.reader(f)
    for row in csv_f:
        name, address, lat, lng = row
        if crud.get_location_by_name(name) == None:
            loc_obj = crud.create_location(name, float(lat), float(lng), address)
            locs_in_db.append(loc_obj)
    print(locs_in_db)

def seed_cities(filename):
    """Add new sample cities to Location table."""

    f = open(filename)
    csv_f = csv.reader(f)
    for row in csv_f:
        city, state, country, lat, lng = row
        if crud.get_location_by_name(city) == None:
            loc_obj = crud.create_location(city, float(lat), float(lng), city)
            locs_in_db.append(loc_obj)
    print(locs_in_db)


books_in_db = []
def seed_books(filename):
    f2 = open(filename)
    csv_f = csv.reader(f2)
    for row in csv_f:
        web_scraper_order, web_scraper_start_url, link, link_href, title, author, description, genres, isbn, location, cover_path, pub_date = row
        a_num = crud.get_author_id_by_name(author)
        author_num = int(a_num[0])
        test_loc_id = 1
        # if location != None:
        #     l_num = crud.get_location_id_by_name(location)
        #     location_num = int(l_num[0])
        #     print(l_num)
        #     print(location_num)
        book_obj = crud.create_book(title, author_num, description, cover_path, isbn)
    
        books_in_db.append(book_obj)
    print(books_in_db)


book_locs_in_db = []
def seed_book_locs():
    
    # Sample data for multiple locations - Hackbright & Home

    for n in range (1,84):
        book_id = n
        loc_id = 1
        book_obj = crud.create_book_location(book_id, loc_id)
        book_locs_in_db.append(book_obj)

    for n in range (1,84):
        book_id = n
        loc_id = 2
        book_obj = crud.create_book_location(book_id, loc_id)
        book_locs_in_db.append(book_obj)

    for n in range(2,84):
        book_id = n
        loc_id = n
        # if location != None:
        #     l_num = crud.get_location_id_by_name(location)
        #     location_num = int(l_num[0])
        #     print(l_num)
        #     print(location_num)
        book_obj = crud.create_book_location(book_id, loc_id)
        book_locs_in_db.append(book_obj)
    print(book_locs_in_db)


book_genres_in_db = []
def seed_book_genres():
    for n in range(1,80):
        book_id = n
        genre_id = randint(1,39)
        book_obj = crud.create_book_genres(book_id, genre_id)
        book_genres_in_db.append(book_obj)
    print(book_genres_in_db)


#---------------------------------------------------------------------#

if __name__ == '__main__':
    model.connect_to_db(server.app)

    # Create tables if not already created. Delete all existing entries in tables.
    model.db.create_all()

    print("Tables created. Deleting all rows and creating new seed data.")

    # Seed sample data into the database
    seed_authors('data/author_book_data.csv')
    seed_books('data/sv_books.csv')
    seed_addresses('data/addresses.csv')
    seed_cities('data/cities.csv')
    seed_book_locs()
    seed_genres('data/genres.txt')
    seed_book_genres()
    seed_users()
    seed_ratings()

    print("Sample data seeded")