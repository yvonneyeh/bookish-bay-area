# Bookish Bay Area

by [Yvonne Yeh](https://yvonneyeh.com)

**Bookish Bay Area** is a full-stack web application that helps readers find and log books set in the San Francisco Bay Area. This app aims to help readers go on their next literary adventure by allowing them to search for, contribute, and borrow books about the locale, from their local libraries.

## Features

- Displays a list of books set in the Bay Area (Initial database created with Wikipedia, Goodreads list, blog site scraping)
- Has a dropdown list for city/neighborhood subsets
- Provides a text search for books by title/author
- Displays a map with pins indicating locations for each book, with the ability to see the description of the location by clicking the pin
- Shows an image of the book cover and information about the book when hovering on map
- Provides a link to the book’s page on Goodreads
- Allows readers to submit books/locations to be added to the database, and create/edit a list of their favorites or to-read books

## Tech Stack
- **Frontend**: JavaScript, jQuery, HTML5, CSS, Bootstrap, Chart.js
- **Backend**: Python3, Flask, PostgreSQL, SQLAlchemy, Jinja2, Selenium, Bash
- **APIs**: GoodReads, Google Maps

### Why Books? Why Bay Area?
I developed this project at [Hackbright Academy](http://www.hackbrightacademy.com/) for my solo capstone project. I’m a voracious reader and every year, I set a goal to read at least 52 books per year. Every time I encounter a reference to my hometown or somewhere nearby, I get super excited! But I didn’t have a good place to log this information. I grew up in the Silicon Valley and I love exploring the area –– what better way to explore during a global pandemic than through literature? 

My project incorporates everything I’ve learned about full-stack web development in the first 6 weeks of my software engineering fellowship at Hackbright. I started with little to no experience in computer science before this.

### Future Features
- See book’s availability at your local library (Libby/Overdrive API) 

