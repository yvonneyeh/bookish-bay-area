"""Script to seed database."""

import os
from random import choice, randint
from datetime import date, datetime
from faker import Faker
# import pandas as pd
import csv

import crud
import model
import server

os.system('dropdb books')
os.system('createdb books')

fake = Faker()

# f = open('data/silicon_valley_books.csv')
f = open('data/small.csv')
# csv_f = csv.reader(f)
f1 = open('data/test_book_data.csv')
f2 = open('data/silicon_valley_books.csv')


authors_in_db = []
def seed_authors():
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


def seed_users():
    for n in range(10):
        email = f'reader{n}@books.book'
        first_name = fake.first_name()
        last_name = fake.last_name()
        username = f'{first_name}{last_name}'
        password = 'test'
        join_date = datetime.today()
        new_user = crud.create_user(email, first_name, last_name, username, password, join_date)


books_in_db = []
def seed_books():
    csv_f = csv.reader(f2)
    for row in csv_f:
        web_scraper_order, web_scraper_start_url, link, link_href, title, author, description, genres, isbn, location, cover_path, pub_date = row
        # print(author)
        num = crud.get_author_id_by_name(author)
        author_num = int(num[0])
        # print(num)
        # print(author_num)
        # print(author_id)
        # print(author)
        # print(title, author_id, description, cover_path, isbn)
        book_obj = crud.create_book(title, author_num, description, cover_path)
        # print(book_obj)
        # create_book(title, author, description, date, cover)
        books_in_db.append(book_obj)
    print(books_in_db)

#---------------------------------------------------------------------#

if __name__ == '__main__':
    model.connect_to_db(server.app)
    model.db.create_all()

    seed_authors()
    seed_users()
    seed_books()