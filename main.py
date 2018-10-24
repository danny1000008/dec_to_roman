import sqlite3
from flask import g, render_template, request, Flask, current_app
import settings
import datetime
import number
from werkzeug.local import LocalProxy
import logging
from logging.handlers import RotatingFileHandler

#DATABASE = str(settings.DB)
#DATABASE = '/home/dwagstaff24/dannywagstaff.com/roman2/public/new_db.db'
DATABASE = 'new_db.db'
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

app = Flask(__name__)
handler = RotatingFileHandler('roman2.log', maxBytes = 1000, backupCount = 1)  # errors logged to this file
handler.setLevel(logging.WARNING)  # only log errors and above
app.logger.setLevel(logging.WARNING)
#app.logger.addHandler(logging.StreamHandler(stream=sys.stdout))
app.logger.addHandler(handler)  # attach the handler to the app's logger


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    start_value = request.form['startValue'].upper()
    start_type = request.form['numType']
    user_number = number.Number(str(start_value), start_type)
    end_value = ''
    is_roman_valid = None
    check_dec_to_roman = None
    if start_type == 'decimal':
        end_value = user_number.convert_to_roman()
    else:
        end_value = user_number.convert_to_decimal()
        is_roman_valid = user_number.check_if_valid()
        check_dec_to_roman = user_number.convert_to_roman()
    movie_info = None
    movies_that_year = 0
    actor1 = None
    actor1_title_list = None
    actor2 = None
    actor2_title_list = None

    if 1888 <= user_number.decimal <= datetime.date.today().year:
        db = LocalProxy(get_db)
        cur = db.cursor()
        try:
            query = 'SELECT tconst, primaryTitle, genres FROM movies WHERE isAdult = 0 AND titleType = "movie" AND startYear = ?;'
            cur.execute(query, (int(user_number.decimal), ))
            movie_list = cur.fetchall()
        except sqlite3.Error as e:
            app.logger.error('DB call failed. Query = ', query, ' error = ', e)
            print(e)
        try:
            (movie_info, movies_that_year) = user_number.get_random_movie(movie_list)
        except:
            (movie_info, movies_that_year) = (None, 0)

        actor_list = []
        try:
            query = 'SELECT nconst, primaryName, knownForTitles FROM actors WHERE birthYear = ?'
            cur.execute(query, (int(user_number.decimal), ))
            actor_list = cur.fetchall()
        except sqlite3.Error as e:
            print(e)
        if len(actor_list):
            actor1 = list(user_number.get_random_actor2(actor_list))
            print('actor1=', actor1)
            title_IDs = actor1[2].split(',')
            movie_titles = []
            for title_ID in title_IDs:
                try:
                    query = 'select primaryTitle from movies where tconst=?'
                    cur.execute(query, (title_ID, ))
                    db_listing = cur.fetchone()
                    if db_listing:
                        movie_titles.append((title_ID, db_listing))
                except:
                    pass
            actor1.append(movie_titles)

        actor_list = []
        try:
            query = 'SELECT nconst, primaryName, knownForTitles FROM actors WHERE deathYear = ?'
            cur.execute(query, (int(user_number.decimal), ))
            actor_list = cur.fetchall()
        except sqlite3.Error as e:
            print(e)
        finally:
            pass
            #conn.close()
        if len(actor_list):
            #(actor2,  actor2_title_list) = user_number.get_random_actor2(actor_list)
            actor2 = list(user_number.get_random_actor2(actor_list))
            print('actor2=', actor2)
            title_IDs = actor2[2].split(',')
            movie_titles = []
            for title_ID in title_IDs:
                try:
                    query = 'select primaryTitle from movies where tconst=?'
                    cur.execute(query, (title_ID, ))
                    db_listing = cur.fetchone()
                    if db_listing:
                        movie_titles.append((title_ID, db_listing))
                except:
                    pass
            actor2.append(movie_titles)

    '''
    (movie_info, movies_that_year) = user_number.check_for_movies()
    (actor1,  actor2) = user_number.check_for_actors()
    '''
    return render_template('result.html', startValue = start_value, \
        endValue = end_value, movie = movie_info, movieCount = movies_that_year, \
        actor1 = actor1, actor2 = actor2, thisYear = datetime.date.today().year)

def main():
    # I use this for debugging purposes only
    dec_num = Number(1950)
    roman_num = Number("MXXXIX", "roman")
    print("roman=", dec_num.convert_to_roman())
    print("cTD=", roman_num.convert_to_decimal())

if __name__ == '__main__':
    handler = RotatingFileHandler('roman2.log', maxBytes = 1000, backupCount = 1)  # errors logged to this file
    handler.setLevel(logging.WARNING)  # only log errors and above
    app.logger.setLevel(logging.WARNING)
    #app.logger.addHandler(logging.StreamHandler(stream=sys.stdout))
    app.logger.addHandler(handler)  # attach the handler to the app's logger
    #log = logging.getLogger('werkzeug')
    #log.setLevel(logging.DEBUG)
    #log.addHandler(handler)
    app.run(debug = True) # development
    #app.run(debug = False) # production
