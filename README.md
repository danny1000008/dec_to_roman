# dec_to_roman
A Python web application. Type in a base 10 number, and it will be converted to roman numerals, or vice versa. Also, if you choose a number in [1888, current_year], it will show some randomly selected movie and actor information by querying a database (the data came from imdb.com).

# Motivation
This project started out as a project on FreeCodeCamp. I wanted to work on my database skills, so once I had the converter working, I added a small database of movies and actors from imdb.com.  

#Prerequisites
Python 3.x
pip
virtualenv

#Installing
1. Open a shell and cd to the directory where you saved the repo. In a virtual environment, do a `pip install -r requirements.txt` to install packages.
2.Type `python main.py` to start the Flask web server.
3. In a browser window address bar, type `127.0.0.1:5000`. This should open the index page, where you can select a) decimal to roman numerals, b) Roman numerals to decimal. Then type in a valid number in the textbox and click 'Submit' to get `result.html` page.

#Running Tests
1. Type `python tests.py`. Currently only the converter is being tested. I will
add tests for the database connection and queries soon.
