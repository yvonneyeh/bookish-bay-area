"""Script to seed database."""

import os
from random import choice, randint, getrandbits, randrange
from datetime import date, datetime, timedelta
from faker import Faker
from geopy.geocoders import Nominatim
import csv

import crud
import model
import server

os.system('dropdb books')
os.system('createdb books')

fake = Faker()

def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

d1 = datetime.strptime('1/1/2020 1:30 PM', '%m/%d/%Y %I:%M %p')
d2 = datetime.strptime('1/1/2021 4:50 AM', '%m/%d/%Y %I:%M %p')

rand_date = random_date(d1, d2)


# start_date = datetime.date(2020, 1, 1)
# datetime.date(2020-01-01)
# end_date = datetime.date(2021, 3, 1)

# time_between_dates = end_date - start_date
# days_between_dates = time_between_dates.days
# random_number_of_days = random.randrange(days_between_dates)
# random_date = start_date + datetime.timedelta(days=random_number_of_days)

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
    join_date = '2020-03-17 12:34:56'
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

    yg_books = ["Homegoing","Transcendent Kingdom"] 
    yy_books = ["The Circle","Imagine: How Creativity Works","The Pixar Touch: The Making of a Company","Brotopia: Breaking Up the Boys' Club of Silicon Valley"]
    
    for title in yg_books:
        # print(title)
        book_id = crud.get_book_id_by_title(title)
        user_id = 1
        log_date = '2020-07-13'
        # log_date = f"2020-07-13 {randint(0,23)}:{randint(0,59)}:{randint(0,59)}"
        score = 5
        read = True
        my_book = crud.create_rating(user_id, book_id, log_date, score, read)  
        ratings_in_db.append(my_book)


    for title in yy_books:
        # print(title)
        book_id = crud.get_book_id_by_title(title)
        user_id = 1
        log_date = random_date(d1, d2)
        # log_date = f"2020-{randint(1,12)}-{randint(1,30)} {randint(0,23)}:{randint(0,59)}:{randint(0,59)}"
        score = randint(3,5)
        read = True
        my_book = crud.create_rating(user_id, book_id, log_date, score, read)  
        ratings_in_db.append(my_book)

    for n in range(100):
        user_id = randint(1,10)
        book_id = randint(1,80)
        log_date = rand_date = random_date(d1, d2)
        # log_date = datetime.today()
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

    wi_obj = crud.create_author("Walter Isaacson")
    authors_in_db.append(wi_obj)

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

    # wi = crud.get_author_id_by_name("Walter Isaacson")
    # wi_num = int(wi[0])
    # jobs_obj = crud.create_book(title, author_num, description, cover_path, isbn)
    
    # books_in_db.append(jobs_obj)

    print(books_in_db)


book_locs_in_db = []
def seed_book_locs():

    # Sample data for multiple locations - Hackbright & Home
    for n in range (3,84):
        book_id = n
        loc_id = 1
        book_obj = crud.create_book_location(book_id, loc_id)
        book_locs_in_db.append(book_obj)

    for n in range (3,84):
        book_id = n
        loc_id = 2
        book_obj = crud.create_book_location(book_id, loc_id)
        book_locs_in_db.append(book_obj)

    # Sample data for Apple Books
    apple_books = ["Steve Jobs","Apple Confidential 2.0: The Definitive History of the World's Most Colorful Company","Dogfight: How Apple and Google Went to War and Started a Revolution", "Haunted Empire: Apple After Steve Jobs"] 
    apple_locs = ["1 Infinite Loop", "Apple Park", "Apple Central & Wolfe Campus","Apple Garage"]
    n = 0
    for book in apple_books:
        if n < 4:
            book_id = crud.get_book_id_by_title(book)
            loc = apple_locs[n]
            loc_obj = crud.get_location_by_name(loc)
            loc_id = loc_obj.loc_id
            book_obj = crud.create_book_location(book_id, loc_id)
            book_locs_in_db.append(book_obj)
            n += 1

    jobs_locs = ["Steve Jobs' Home","Homestead High School"]
    for loc in jobs_locs:
        book_id = crud.get_book_id_by_title("Steve Jobs")
        loc_obj = crud.get_location_by_name(loc)
        loc_id = loc_obj.loc_id
        book_obj = crud.create_book_location(book_id, loc_id)
        book_locs_in_db.append(book_obj)

    # Sample data for Google Books
    goog_books = ["Are You Smart Enough to Work at Google?","Dogfight: How Apple and Google Went to War and Started a Revolution","Googled: The End of the World as We Know It","Google Speaks","How Google Works","I'm Feeling Lucky: The Confessions of Google Employee Number 59","Planet Google: One Company's Audacious Plan to Organize Everything We Know","The Big Switch: Rewiring the World, from Edison to Google","The Search: How Google and Its Rivals Rewrote the Rules of Business and Transformed Our Culture","What Would Google Do?","Work Rules!: Insights from Inside Google That Will Transform How You Live and Lead"]
    goog_locs = ["Googleplex","Google X Lab","Google SF","Google RWC","Google Sunnyvale","Google Garage"]
    n = 0
    for book in goog_books:
        if n < 6:
            book_id = crud.get_book_id_by_title(book)
            loc = goog_locs[n]
            loc_obj = crud.get_location_by_name(loc)
            loc_id = loc_obj.loc_id
            book_obj = crud.create_book_location(book_id, loc_id)
            book_locs_in_db.append(book_obj)
            n += 1


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


def add_yy_books():
    homegoing = 1
    t_kingdom = 2
    stanford = 3
    tofu_house = 4
    hg_obj = crud.create_book_location(homegoing, stanford)
    tk_obj1 = crud.create_book_location(homegoing, stanford)
    tk_obj2 = crud.create_book_location(homegoing, tofu_house)
    book_locs_in_db.append(hg_obj)
    book_locs_in_db.append(tk_obj1)
    book_locs_in_db.append(tk_obj2)
    


#---------------------------------------------------------------------#

if __name__ == '__main__':
    model.connect_to_db(server.app)

    # Create tables if not already created. Delete all existing entries in tables.
    model.db.create_all()

    print("Tables created. Deleting all rows and creating new seed data.")

    # Seed sample data into the database
    seed_authors('data/authors.csv')
    seed_books('data/sv_books.csv')
    seed_addresses('data/addresses.csv')
    seed_cities('data/cities.csv')
    seed_book_locs()
    seed_genres('data/genres.txt')
    seed_book_genres()
    seed_users()
    seed_ratings()
    add_yy_books()

    print("Sample data seeded")