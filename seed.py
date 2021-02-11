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

f = open('data/silicon_valley_history_books.csv')
csv_f = csv.reader(f)


for row in csv_f:
    web_scraper_order, web_scraper_start_url, link, link_href, title, author, description, genres, isbn, location, cover, date = row
    print(author)
    # author = row[5]
    # print(row[5])

# Load movie data from CSV file
# book_data = pd.read_csv('data/silicon_valley_history_books.csv')

# authors_data = pd.read_csv('data/silicon_valley_history_books.csv', names="authors", index=False, header=False)
# lil_data = pd.read_csv('small.csv')
# print(lil_data['author'][0])

# authors_in_db = []
# for author in lil_data:
#     name = lil_data.author[0]
#     print(name)
    # author_obj = crud.create_author(name)
    # authors_in_db.append(author_obj)
    # print(authors_in_db)



# print(lil_data['author'].astype('string'))
# print(lil_data['author'].apply('str'))
# print(lil_data['author'])
# print(lil_data.author.astype('str'))
# print(lil_data.author.apply('str'))


# object['<key>'].astype('str') or object.<key>.apply('str')

# print(authors_data)
# print(authors_data.authors)


# print(book_data.title)

# authors_in_db = []
# for author in book_data:
#     name = book_data.author
#     print(name)
    # author_obj = crud.create_author(name)
    # authors_in_db.append(author_obj)

# for n in range(10):
#     email = f'reader{n}@books.com'
#     password = 'test'

#     new_reader = crud.create_reader(email, password)








# book = create_book(title, author_id, description, pub_date, cover_path, isbn, pages)


# books_in_db = []
# for book in book_data:
#     # Get the title, overview, and poster_path from the movie dictionary.
#     title = book_data.title


#     overview = movie.get('overview')
#     poster_path = movie.get('poster_path')

#     # Get the release_date and convert it to a datetime object with datetime.strptime
#     release_date = datetime.strptime(movie.get('release_date'), '%Y-%m-%d')

#     # Create movie instances
#     movie_obj = crud.create_movie(title, overview, release_date, poster_path)

#     # Append movie object to movies_in_db list
#     movies_in_db.append(movie_obj)

# # result = {}
# # for row in book_data:
# #     for column, value in row.items():
# #         result.setdefault(column, []).append(value)
# # print(result)

# title


# # book_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
# # title = db.Column(db.String)
# # author_id = db.Column(db.Integer, db.ForeignKey('authors.author_id'))
# # description = db.Column(db.Text)
# # pub_date = db.Column(db.DateTime)
# # cover_path = db.Column(db.String)
# # isbn = db.Column(db.Integer)
# # pages = db.Column(db.Integer)

# # test_reader = Reader(first_name = 'Yvonne',
# #             last_name = 'Yeh',
# #             email = 'email@email.com',
# #             password = 'test'
# #             )

# # >>> db.session.add(mov)
# # >>> db.session.commit()

# # test_reader = Reader(first_name = 'Yvonne', last_name = 'Yeh', email = 'email@email.com', password = 'test')
# # test_book = Book(title='BookTitle', author_id = 1)
# # test_author = Author(author_id = 1, first_name='AA', last_name='BB')

# # rate = Rating(book_id=4, user_id=1, score=5)

# #  rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
# #     book_id = db.Column(db.Integer, db.ForeignKey('books.book_id'))
# #     user_id = db.Column(db.Integer, db.ForeignKey('readers.user_id'))
# #     log_date = db.Column(db.DateTime)
# #     score = db.Column(db.Integer)