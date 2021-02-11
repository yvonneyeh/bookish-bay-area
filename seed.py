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

model.connect_to_db(server.app)
model.db.create_all()

fake = Faker()

f = open('data/silicon_valley_books.csv')
csv_f = csv.reader(f)

authors_in_db = []
for row in csv_f:
    web_scraper_order, web_scraper_start_url, link, link_href, title, author, description, genres, isbn, location, cover, date = row
    # if crud.get_author_by_name(author) != None:
    #     print(author)
    # else:
    author_obj = crud.create_author(author)
    authors_in_db.append(author_obj)
# print(authors_in_db)

test_user = model.User(
                        username = 'yvonneyeh',
                        first_name = 'Yvonne',
                        last_name = 'Yeh',
                        email = 'email@email.email',
                        password = 'test'
                        )

for n in range(10):
    email = f'reader{n}@books.book'
    first_name = fake.first_name()
    last_name = fake.last_name()
    username = f'{first_name}{last_name}'
    password = 'test'
    join_date = datetime.today()
    new_user = crud.create_user(email, first_name, last_name, username, password, join_date)


# book = create_book(title, author_id, description, pub_date, cover_path, isbn, pages)

books_in_db = []
for row in csv_f:
    web_scraper_order, web_scraper_start_url, link, link_href, title, author, description, genres, isbn, location, cover_path, pub_date = row
    x = crud.get_author_id_by_name(author)
    author_id = int(x[0])
    # pub_date = datetime.strptime(date('release_date'), '%Y-%m-%d')
    # print(pub_date)
    book_obj = crud.create_book(title, author_id, description, cover_path, isbn)
    # create_book(title, author, description, date, cover, isbn)
    books_in_db.append(book_obj)
print(books_in_db)





# test_user = User(first_name = 'Yvonne', last_name = 'Yeh', email = 'email@email.com', password = 'test')
# test_book = model.Book(title='BookTitle', author_id = 1)
# test_author = model.Author(author_id = 1, name='Author Author')

# test_rate = model.Rating(book_id=4, username=yvonneyeh, score=5)

model.db.session.add(test_user)
# model.db.session.add(test_rate)
# model.db.session.add(test_book)
# model.db.session.add(test_author)

model.db.session.commit()