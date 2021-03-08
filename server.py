"""Server for Bookish Bay Area app."""

import os
from flask import (Flask, render_template, request, flash, session, redirect, jsonify)
from model import (db, connect_to_db, User, Book, Rating, Author, BookAuthor, Genre, BookGenre, Location, BookLocation)
from sqlalchemy_searchable import search
from datetime import date, datetime
from random import randint
import faker
import crud
import helper

from jinja2 import StrictUndefined

MAPS_JS_KEY = os.environ['MAPS_JS_KEY']

app = Flask(__name__)
app.secret_key = "dev"
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def homepage():
    """View homepage."""

    return render_template('homepage.html')


# ---------- ACCOUNT ROUTES ---------- #

@app.route("/register")
def reg_form():
    """Display registration form"""

    return render_template("register.html")


@app.route("/register", methods=["POST"])
def register_user():
    """Creates new user if user does not yet exist"""

    username = request.form.get("username")
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    # Validate if username or email already exists in users table in database
    if not crud.get_user_by_email_id(email, username):

        user = User(username=username, email=email, first_name=first_name, last_name=last_name, password=password)

        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash("User created!")

        return redirect("/login")

    # If account does exist, flash message to indicating email or username exists.
    else:
        if User.query.filter_by(email=email).all():
            flash(f"There's already an account associated with {email}")
        else:
            flash(f"The username {username} is already taken")

        return redirect("/register")


@app.route('/login')
def login():
    """View Login page."""

    return render_template('login.html')


@app.route('/login', methods=['POST'])
def log_in_user():
    """Login user and redirect to homepage."""

    username = request.form.get('username')
    password = request.form.get('password')

    user_object = crud.get_user_by_username(username)

    if user_object != None:
        if password == user_object.password != None:
            session['username'] = user_object.username
            session['user_id'] = user_object.user_id
            # print('Logged in!')
            flash('Logged in!')
        else:
            flash('Incorrect password') 
            return redirect("/login")  
    else:
        flash('Username does not exist. Please register for an account.')
        return redirect("/register")
    
    return redirect('/')


@app.route("/account/update_info")
def show_acct_info_form():
    """Display form for user to update account information"""

    if "user_id" in session:
        user = User.query.get(session.get("user_id"))

        return render_template("/user_info.html", user=user)

    else:
        flash("You need to be logged in to access that page")

        return redirect("/login")


@app.route("/account/update_info", methods=["POST"])
def update_account_info():
    """Update a user's account information"""

    if "user_id" in session:
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        username = request.form.get("username")
        email = request.form.get("email")
        bio = request.form.get("bio")
        
        user = User.query.get(session["user_id"])

        # Form fields are not required - only update database if text was
        # entered in that field and not the same as what's already in the db
        if len(first_name) > 0 and first_name != user.first_name:
            user.first_name = first_name

        if len(last_name) > 0 and last_name != user.last_name:
            user.last_name = last_name

        if len(username) > 0 and username != user.username:
            user.username = username

        if len(email) > 0 and email != user.email:
            user.email = email

        if len(bio) > 0 and bio != user.bio:
            user.bio = bio

        db.session.add(user)
        db.session.commit()

        flash("Information updated!")

        return redirect("/account/update_info")

    else:
        flash("You need to be logged in to access that page")

        return redirect("/login")


@app.route("/account/change_password")
def show_change_pass_form():
    """Show form for users to change their password"""

    if "user_id" in session:
        return render_template("update_password.html")

    else:
        flash("You need to be logged in to access that page")
        return redirect("/login")


@app.route("/account/change_password", methods=["POST"])
def change_user_password():
    """Change a user's password"""

    if "user_id" in session:
        old_pass = request.form.get("oldpass")
        new_pass = request.form.get("newpass")

        user = User.query.get(session["user_id"])

        if user.check_password(old_pass):
            user.set_password(new_pass)

            db.session.add(user)
            db.session.commit()

            flash("Password successfully updated")

            return redirect("/account/change_password")

        else:
            flash("Incorrect password, please try again")

            return redirect("/account/change_password")

    else:
        flash("You need to be logged in to access that page")

        return redirect("/login")


@app.route("/account/saved_books")
def display_saved_books():
    """Display a user's saved books"""

    if "username" in session:
        username = session.get("username")
        ratings = crud.get_user_ratings(username)

        return render_template("user_read.html",
                               read_books=ratings)

    else:
        flash("You need to be logged in to access that page")

        return redirect("/login")


@app.route("/account/read_books")
def display_read_books():
    """Display a user's read/rated books"""

    # Query database to find Ratings objects belonging to user
    # & not marked read
    if "user_id" in session:
        user_id = session.get("user_id")
        read_.get_users_rated_books(user_id)

        return render_template("user_read.html",
                               read_books=read_books)

    else:
        flash("You need to be logged in to access that page", "error")

        return redirect("/login")


@app.route("/account/locations")
def display_user_booklocs():
    """Display a user's saved book locations"""

    if "user_id" in session:
        user_id = session.get("user_id")
        read_books = helper.get_users_rated_books(user_id)
        location_dict, location_list = helper.get_booklocs_by_user(user_id)

        return render_template("user_locs.html",
                               read_books=read_books,
                               book_locations=location_dict,
                               location_list=location_list,  
                               MAPS_JS_KEY=MAPS_JS_KEY)

        # author = crud.get_author_name_by_book_id(book_id)
        # book = crud.get_book_by_id(book_id)
        # location_dict, location_list = helper.get_locations(book_id)

        # return render_template("book_details.html", 
        #                     author=author, 
        #                     book=book,
        #                     book_locations=location_dict,
        #                     location_list=location_list, 
        #                     )

    else:
        flash("You need to be logged in to access that page", "error")

        return redirect("/login")


@app.route('/users')
def all_users():
    """Display all users."""
    users = crud.get_all_users()

    return render_template("all_users.html", users=users)


@app.route('/users', methods=['POST'])
def create_account():
    """Create a new user account."""

    username = request.form.get('username')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    password = request.form.get('password')
    join_date = datetime.today()

    if crud.get_user_by_email(email) != None:
        flash('Email exists. Please sign up with a different email.')
    else:
        crud.create_user(email, first_name, last_name, username, password, join_date)
        flash('Account created successfully!')

    return redirect('/')


@app.route('/users/profile')
def show_logged_in_user_profile():
    """Show details for a logged-in user"""

    if "username" in session:
        username = session["username"]
        user = crud.get_user_by_username(username)
        ratings = crud.get_user_ratings(username) 

        return render_template("/user_details.html", user=user, ratings=ratings)

    else:
        flash("You need to be logged in to access that page")

        return redirect("/login")



@app.route('/users/<username>')
def show_user(username):
    """Show details for a user"""
    user = crud.get_user_by_username(username)
    ratings = crud.get_user_ratings(username)

    return render_template("user_details.html", user=user, ratings=ratings)


@app.route("/logout")
def log_out_user():
    """Log out user"""

    if "user_id" in session:
        del session["user_id"]
        flash("Logged out")

    return redirect("/")


# ---------- BOOK ROUTES ---------- #

@app.route('/books')
def show_book_list():
    """Show list of books. 
    If user selected genre: filter by genre.
    Else: If user entered title search, filter by title
    Else: display entire book list.
    """
    
    user_genre = None
    user_title_search = None
    user_author_search = None
    user_search = None
    # books = []

    if 'genre' in request.args:
        user_genre = request.args['genre']
        books = helper.get_books_by_genre(user_genre)

    else: 
        books = crud.get_all_books()

    
    if 'user_search' in request.args:
        user_title_search = request.args['user_search']
        books = helper.get_books_by_search(user_search)

        if books == None:
            flash('No results found')
    
    else: 
        books = crud.get_all_books()


    if 'title_search' in request.args:
        user_title_search = request.args['title_search']
        books = helper.get_books_by_title(user_title_search)
        # print("search", len(books))

        if books == None:
            flash('No results found')
    
    else: 
        books = crud.get_all_books()
        # print(len(books))

    # if 'author_search' in request.args:
    #     user_author_search = request.args['author_search']
    #     books = helper.get_books_by_author(user_author_search)

    #     if books == None:
    #         flash('No results found')
        
    # else: 
    #     books = crud.get_all_books()

    # print("final", len(books))
    return render_template("all_books.html", 
                            books=books, 
                            genre=user_genre)


@app.route('/<int:book_id>')
def show_book(book_id):
    """Show details for a book."""
    
    author = crud.get_author_name_by_book_id(book_id)
    book = crud.get_book_by_id(book_id)
    locations = crud.get_all_locations()
    location_dict, location_list = helper.get_locations(book_id)

    return render_template("book_details.html", 
                            author=author, 
                            book=book,
                            locations = locations,
                            book_locations=location_dict,
                            location_list=location_list, 
                            MAPS_JS_KEY=MAPS_JS_KEY)


@app.route('/books/<int:book_id>', methods=["POST"])
def create_book_location_on_details_page(book_id):
    # """Show details for a book."""
    
    location = request.form.get('location')
    loc = crud.get_location_id_by_name(location)

    if loc == None:
        flash("Select a Title")
        
        return redirect(f"/books/{book_id}")
    
    else:
        # book_id = crud.get_book_id_by_title(title)
        # print(loc)
        # print(type(loc))
        loc_id = loc.loc_id

        crud.create_book_location(book_id, loc_id)
        flash('New Book Location submitted successfully!')

    return redirect(f"/books/{book_id}")

    # author = crud.get_author_name_by_book_id(book_id)
    # book = crud.get_book_by_id(book_id)
    # location_dict, location_list = helper.get_locations(book_id)

    # return render_template("book_details.html", 
    #                         author=author, 
    #                         book=book,
    #                         book_locations=location_dict,
    #                         location_list=location_list, 
    #                         MAPS_JS_KEY=MAPS_JS_KEY)


@app.route('/user/save-book', methods=["POST"])
def save_book_to_user_list():
    """Instantiate a Rating (User-Book) instance."""

    if "user_id" in session:
        book_id = request.form.get("book_id")

        saved_book = Rating(user_id=session["user_id"], book_id=book_id)

        db.session.add(saved_book)
        db.session.commit()

        return "Book added"

    else:
        return "You must sign in to save books"


@app.route("/user/unsave-book", methods=["POST"])
def unsave_book_to_user_list():
    """Remove a User-Book instance"""

    book_id = request.form.get("book_id")

    if "user_id" in session:
        user_id = session.get("user_id")
        book_to_delete = helper.get_rating_by_ids(user_id, book_id)

        db.session.delete(book_to_delete)
        db.session.commit()

        return "Book removed"

    else:
        return "You must sign in to edit saved books"


@app.route("/user/read-book", methods=["POST"])
def mark_saved_book_as_read():
    """Update a Rating's 'read' attribute to True"""

    if "user_id" in session:
        book_id = int(request.form.get("book_id"))
        user_id = session["user_id"]

        saved_book = helper.get_users_saved_book(user_id, book_id)

        if saved_book:
            saved_book.read = True

            db.session.add(saved_book)
            db.session.commit()

        else:
            saved_book = Rating(user_id=user_id, 
                                book_id=book_id,
                                read=True)

            db.session.add(saved_book)
            db.session.commit()

        return "Book marked as read"

    else:
        return "You must be signed in to save books"


@app.route("/user/unread-book", methods=["POST"])
def unmark_saved_book_as_read():
    """Update a Rating's 'read' attribute to False"""

    if "user_id" in session:

        book_id = int(request.form.get("book_id"))

        saved_book = helper.get_session_users_saved_book(user_id, book_id)

        saved_book.read = False

        db.session.add(saved_book)
        db.session.commit()

        return "Book marked as not read"


@app.route("/user/is-book-saved/<int:book_id>")
def check_if_book_saved_for_user(book_id):
    """For a given user, check if a book is saved in user_books"""

    user_id = session.get("user_id")

    if user_id:
        ub = helper.get_rating_by_ids(user_id, book_id)

        response = {}

        if ub:
            response["saved"] = True
            if ub.read:
                response["read"] = True
            else:
                response["read"] = False
        else:
            response["saved"] = False
            response["read"] = False

    return jsonify(response)


# ---------- AUTHOR ROUTES ---------- #

@app.route('/authors')
def all_authors():
    """Display all authors."""
    authors = crud.get_all_authors()

    return render_template("all_authors.html", authors=authors)


@app.route('/authors/<int:author_id>')
def show_author(author_id):
    """Show details for an author."""
    
    author = crud.get_author_by_id(author_id)

    return render_template("author_details.html", author=author)


# ---------- LOCATION ROUTES ---------- #

@app.route('/books/map')
def show_book_map(book_id):
    """Show all book locations on a map."""
    
    location_dict, location_list = helper.get_all_locations()

    # print("*"*20)
    # print(f"book_locations={location_dict}, \n location_list={location_list}" )

    return render_template("book_map.html", 
                            book_locations=location_dict,
                            location_list=location_list, 
                            MAPS_JS_KEY=MAPS_JS_KEY)

@app.route('/library-map')
def show_library_map():
    """View Map."""

    return render_template('library_map.html', MAPS_JS_KEY=MAPS_JS_KEY)

@app.route('/locations')
def all_locations():
    """Show list of books. 
    If user entered location search, filter by location
    Else: display entire book list.
    """

    user_loc_search = None

    if 'loc_search' in request.args:
        user_loc_search = request.args['loc_search']
        locations = helper.get_locations_by_search(user_loc_search)

        if locations == None:
            flash('No results found')
    
    else: 
        locations = crud.get_all_locations()

    return render_template("all_locations.html", locations=locations)


@app.route('/locations/<int:loc_id>')
def show_location(loc_id):
    """Show details for a location."""
    
    location = crud.get_location_by_id(loc_id)
    # book_dict, book_list = helper.get_books_by_location(loc_id)

    return render_template("loc_details.html", 
                            location=location, 
                            # books = book_dict, 
                            # books_list = book_list,
                            MAPS_JS_KEY=MAPS_JS_KEY)


# ---------- GENRE ROUTES ---------- #

@app.route('/genres')
def all_genres():
    """Display all genres."""
    genres = crud.get_all_genres()

    return render_template("all_genres.html", genres=genres)

@app.route('/genres/<int:genre_id>')
def show_genre(genre_id):
    """Show details for a genre."""
    
    genre = crud.get_genre_by_id(genre_id)

    return render_template("genre_details.html", genre=genre)

# ---------- RATING ROUTES ---------- #


@app.route('/ratings')
def all_ratings():
    """Display all ratings."""
    ratings = crud.get_all_ratings()

    return render_template("all_ratings.html", ratings=ratings)


@app.route('/ratings/<int:rating_id>')
def show_rating(rating_id):
    """Show details for a location."""
    
    rating = crud.get_rating_by_id(rating_id)

    return render_template("rating_details.html", 
                            rating=rating)


# ---------- SUBMISSION FORM ROUTES ---------- #

@app.route('/add/location')
def show_new_loc_form():
    """Display new location submission form."""

    return render_template("add_loc.html")


@app.route('/add/location', methods=['POST'])
def create_new_user_submitted_location():
    """Create a new user-submitted location."""

    name = request.form.get('name')
    address = request.form.get('address')

    helper.create_user_submitted_loc(name, address)
    flash('Location submitted successfully!')

    return redirect('/locations')


@app.route('/add/book-loc')
def show_new_book_loc_form():
    """Display new book-location submission form."""

    books = crud.get_all_books()
    locations = crud.get_all_locations()

    return render_template("add_bookloc.html",
                            books = books,
                            locations = locations)


@app.route('/add/book-loc', methods=['POST'])
def create_new_book_location():
    """Create a new user-submitted book-location."""

    title = request.form.get('title')
    location = request.form.get('location')

    # return title, location
    # print(title)
    # print(location)

    if title == None or location == None:
	    flash("Select a Title & Location")
        # return redirect("/add/book-loc")
    elif title == None:
	    flash("Select a Title")
        # return redirect("/add/book-loc")
    elif location == None:
	    flash("Select a Location")
        # return redirect("/add/book-loc")
	
    else:
        book_id = crud.get_book_id_by_title(title)
        loc_id = crud.get_location_id_by_name(location)

        bookloc = crud.create_book_location(book_id, loc_id)
        flash('New Book Location submitted successfully!')

    print(bookloc)
    return redirect('/books')

    # title = request.form['book']
    # book_id = crud.get_book_id_by_title(title)

    # if book:
    #     return jsonify({'country':country})
    #     flash('Location submitted successfully!')

    # return jsonify({'error': 'missing data..'})

    # crud.create_book_location(book_id, loc_id)
    
    # return redirect('')


# ---------- SEARCH ROUTES ---------- #

@app.route("/search")
def display_search_results():
    """Display search results"""

    return render_template("search.html", MAPS_JS_KEY=MAPS_JS_KEY)


# ---------- AJAX / JSON ROUTES ---------- #

@app.route("/user/loggedin")
def is_user_logged_in():
    """Check if user is logged in"""

    if "user_id" in session:
        return "true"

    else:
        return "false"


@app.route('/json/book-titles')
def get_book_titles_for_form():

    res = Book.query.all()
    books = [r.as_dict() for r in res]
    
    return jsonify(books)


@app.route("/json/search")
def return_json_search_results():
    """Search for books given a location, 
    seed books into database, 
    and return json response."""

    search_terms = request.args.get("search")
    lat_long = helper.call_geocoding_api(search_terms)

    if lat_long != "Invalid search terms":
        # response = call_geocoding_api(lat_long)
        # crud.create_book(response)

        json_response = jsonify(response["books"])

        return json_response

    else:
        return "Invalid search terms"


@app.route("/json/search-coords")
def get_search_coordinates():
    """Call Google Maps Geocoding API with search terms & return json
    of coordinates"""

    search_terms = request.args.get("search")
    lat_long = helper.call_geocoding_api(search_terms)

    if lat_long != "Invalid search terms":
        return jsonify(lat_long)

    else:
        return "Invalid search terms"


if __name__ == '__main__':
    connect_to_db(app)
    app.run(host='0.0.0.0', debug=True)