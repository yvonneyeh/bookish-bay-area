"""Script to seed database."""

import os
from random import choice, randint
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


def seed_users():
    for n in range(10):
        email = f'reader{n}@books.book'
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f'{first_name}{last_name}'
        password = 'test'
        join_date = datetime.today()
        new_user = crud.create_user(email, first_name, last_name, username, password, join_date)

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
def seed_locations(filename):
    """Add new locations to Location table."""

    f = open(filename)
    csv_f = csv.reader(f)
    for row in csv_f:
        city, state, country, lat, lng = row
        if crud.get_location_by_name(city) == None:
            loc_obj = crud.create_location(city, float(lat), float(lng))
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
        # if location != None:
        #     l_num = crud.get_location_id_by_name(location)
        #     location_num = int(l_num[0])
        #     print(l_num)
        #     print(location_num)
        book_obj = crud.create_book(title, author_num, description, cover_path, isbn)
    
        books_in_db.append(book_obj)
    print(books_in_db)

#---------------------------------------------------------------------#

if __name__ == '__main__':
    model.connect_to_db(server.app)
    model.db.create_all()

    
    seed_locations('data/cities.csv')
    seed_genres('data/genres.txt')
    seed_authors('data/author_book_data.csv')
    seed_books('data/sv_books.csv')
    seed_users()