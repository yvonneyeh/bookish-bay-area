"""Script to seed database."""

import os
from random import choice, randint
from datetime import datetime
# import pandas as pd
import csv

import crud
import model
import server

os.system('dropdb books')
os.system('createdb books')

model.connect_to_db(server.app)
model.db.create_all()

f = open('data/silicon_valley_books.csv')
csv_f = csv.user(f)

authors_in_db = []
for row in csv_f:
    web_scraper_order, web_scraper_start_url, link, link_href, title, author, description, genres, isbn, location, cover, date = row
    author_obj = crud.create_author(author)
    authors_in_db.append(author_obj)
print(authors_in_db)


for n in range(10):
    email = f'reader{n}@books.com'
    password = 'test'
    new_user = crud.create_user(email, password)


# book = create_book(title, author_id, description, pub_date, cover_path, isbn, pages)

# books_in_db = []
# for row in csv_f:
#     web_scraper_order, web_scraper_start_url, link, link_href, title, author, description, genres, isbn, location, cover, date = row
#     # pub_date = datetime.strptime(date('release_date'), '%Y-%m-%d')
#     # print(pub_date)
#     book_obj = crud.create_book(title, author, description, date, cover, isbn)
#     authors_in_db.append(book_obj)
# print(books_in_db)


test_user = model.Reader(first_name = 'Yvonne',
            last_name = 'Yeh',
            email = 'email@email.com',
            password = 'test'
            )


# test_user = Reader(first_name = 'Yvonne', last_name = 'Yeh', email = 'email@email.com', password = 'test')
test_book = model.Book(title='BookTitle', author_id = 1)
test_author = model.Author(author_id = 1, name='Author Author')

rate = model.Rating(book_id=4, user_id=1, score=5)

model.db.session.add(test_user)
model.db.session.add(test_book)
model.db.session.add(test_author)
model.db.session.commit()