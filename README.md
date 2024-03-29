# Bookish Bay Area

by [Yvonne Yeh](https://yvonneyeh.com)

**Bookish Bay Area** is a full-stack web app that helps readers find and log books set in the San Francisco Bay Area. This app aims to help readers go on their next literary adventure by allowing them to search for, save, and contribute books then borrow those books from their local libraries.

[Bookish Intro Video](https://www.youtube.com/watch?v=R-Wqe7G9UL4)

![Screenshot of Homepage](https://raw.githubusercontent.com/yvonneyeh/bookish-bay-area/master/static/img/homepage.png)


### Table of Contents
- [Why Bookish](#Why)
- [App Features](#Features)
- [Technology](#Tech)
- [Initial Seed Data](#Seed)
- [BookSpot & Library Maps](#Map)
- [Data Structure](#Data)
- [Installation Instructions](#Install)
- [Future Features](#Future)
- [Acknowledgments](#Acknowledgments)


## <a name="Why"></a>Bookish? Why Books? Why Bay Area?
I developed this project at [Hackbright Academy](http://www.hackbrightacademy.com/) for my solo capstone project. As a voracious reader, I read at least 52 books per year, and every time I encounter a reference to my hometown or somewhere nearby, I get super excited! But I didn’t have a good place to log this information. I grew up in the Silicon Valley and I love exploring the area –– what better way to explore during a global pandemic than through literature? 

My project incorporates everything I’ve learned about full-stack web development in the first 6 weeks of my software engineering fellowship at Hackbright. I started with little to no experience in computer science before this and was excited to combine my bookishness, love of exploration, and new coding skills to build a tool I've always wanted to use personally.

![GIF of BookSpots Map](https://raw.githubusercontent.com/yvonneyeh/bookish-bay-area/master/static/img/bookspots.gif)

## <a name="Features"></a>Features

- Displays a list of books set in the Bay Area about Silicon Valley and the tech industry
- Has a dropdown list for city/neighborhood/location subsets
- Provides a text search for books by title/author/location
- Displays a map with pins indicating locations for each book location (BookSpot) with Google Maps API
- Renders a map of the specific location of the user and nearby libraries with the browser's HTML5 Geolocation feature along with the Maps JavaScript API
- Shows book details (including the author, an image of the cover, and a link to more information about the book on Goodreads) and shows all BookSpots on a Google Map with custom map marker pins
- Allows readers to submit new books to be added to the database, and create/edit a list of their read, rated, and saved books
- Geocoding user-submitted locations into coordinates to save to the location database
- Allows readers to contribute new BookSpot (add books to a location or add locations to a book)
- See all ratings of books rendered in a graph with Chart.js
- Users can save their favorite location and receive email alerts when a new book is added via SendGrid API and web push notifications via OneSignal.

![Web Push Notifications with OneSignal](https://raw.githubusercontent.com/yvonneyeh/bookish-bay-area/master/static/img/notifications.gif)
*User Profile & Web Push Notifications with OneSignal*

## <a name="Tech"></a>Tech Stack
- **Frontend**: JavaScript, jQuery, HTML5, CSS, Bootstrap, Chart.js
- **Backend**: Python3, Flask, PostgreSQL, SQLAlchemy, Jinja2, Selenium, Bash
- **APIs**: Open Library, Google Maps, Google Places, Google Geocoding, Nominatim OpenStreetMap, Twilio SendGrid, OneSignal, Libby, OverDrive, GoodReads (deprecated, see [data collection section](#Seed) below)

## <a name="Seed"></a>Initial Seed Data Collection

![GIF of Book Search](https://raw.githubusercontent.com/yvonneyeh/bookish-bay-area/master/static/img/book-search.gif)

There’s currently no API for book-locations, I solved this by learning to scrape data from multiple sources together with Selenium WebDriver to build an initial SQL database. The seed data was scraped and parsed from GoodReads, Amazon, Wikipedia, and literature blogs, using Selenium WebDriver and Beautiful Soup. Selenium was used to call a GET request for book searches, then used to automate the process of scrolling down the page, prompting sites' lazy load to render more posts. The HTML from the search was then parsed using Beautiful Soup to extract the data about each book, including: title, author, description, genres, ISBN, setting or location (if available), cover image, date published, and link to GoodReads. This process of web-scraping was chosen because GoodReads' API was recently deprecated, with all existing API keys disabled and unsupported as of December 2020. By scraping the data, I was able to gather information about books from location-specific lists and articles, such as [Silicon Valley History](https://www.goodreads.com/list/show/13430.Silicon_Valley_History) list on GoodReads and [Books](https://en.wikipedia.org/wiki/Category:Books_about_California)/[Novels](https://en.wikipedia.org/wiki/Category:Novels_set_in_California) set in California from Wikipedia. 

## <a name="Map"></a>BookSpot & Library Maps

![Book Details page for 'Steve Jobs' by Walter Isaacson](https://raw.githubusercontent.com/yvonneyeh/bookish-bay-area/master/static/img/steve-jobs.png)
*Book Details Page*

![Location Details page for Stanford University](https://raw.githubusercontent.com/yvonneyeh/bookish-bay-area/master/static/img/stanford.png)
*Location Details Page*

![Library Map](https://raw.githubusercontent.com/yvonneyeh/bookish-bay-area/master/static/img/libraries.png)
*Local Library Map*

## <a name="Data"></a>Data Structure

![Data Model Graphic](https://raw.githubusercontent.com/yvonneyeh/bookish-bay-area/master/static/img/data-model.png)

## <a name="Install"></a>Installation Instructions

### Prerequisites
To run Bookish, you will need the following API keys: 
- [Google Maps Geocoding](https://developers.google.com/maps/documentation/geocoding/start)
- [Google Maps JavaScript](https://developers.google.com/maps/documentation/javascript/tutorial)
- [SendGrid Mail Send API](https://sendgrid.com/docs/api-reference/)

**Python3** and **PostgreSQL** will also need to be installed on your machine.

### Running Bookish

1. Clone this repository:
```shell
git clone https://github.com/yvonneyeh/bookish-bay-area.git
```

***Optional***: Create and activate a virtual environment:
```shell
pip3 install virtualenv
virtualenv env
source env/bin/activate
```

2. Install dependencies: 
```shell
pip3 install -r requirements.txt
```

3. Create environmental variables to hold your API keys in a `secrets.sh` file:
```
export MAPS_JS_KEY='{MAPS_JS_KEY}'
export MAPS_GEOCODING_KEY='{MAPS_GEOCODING_KEY}'
export SENDGRID_API_KEY='{SENDGRID_API_KEY}' #OPTIONAL
```

4. Create your database & seed sample data:
```shell
createdb books
python3 seed.py
```

5. Run the app on localhost:
```shell
source secrets.sh
python3 server.py
```

## <a name="Future"></a>Future Features
- See book’s availability at your local library (Libby/Overdrive API) 
- Location-based notifications with geofencing (Google Maps API)
- Literary walking tours built from user's bookmarked locations


## <a name="#Acknowledgments"></a>Acknowledgments 
In addition to the support of my family, friends, partner, and fellow Hackbright cohort-mates, the following people were instrumental to this project, providing mentorship, code reviews, inspiration, and guidance:

#### Hackbright Advisors
- Andrew Blum
- Kat Huber-Juma
- Thu Nguyen
- Lucia Racine

#### Amiga Housemates
- Elizabeth Jamison
- Fionnie Pollack
- Katie Aquino
- Nan Li

#### Mentors
- Lydia Gorham
- Katie Cheng
- Meghan Hade