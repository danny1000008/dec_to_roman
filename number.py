#import pymysql.cursors
import sqlite3
import os
import random
import settings

class Number():
    """docstring for ."""
    def __init__(self, num, num_type = 'decimal'):
        self.decimal = None
        self.roman = None
        self.number_movies = None
        self.movie = None
        if num_type == "roman" and type(num) == str:
            self.roman = num
            self.decimal = self.convert_to_decimal()
        else: # num_type == 'decimal':
            self.decimal = int(num)
            #self.roman = self.convert_to_roman()

    def convert_to_decimal(self):
        dec = 0
        arrDec = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        arrRoman = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V",
            "IV", "I"]
        roman_value = self.roman
        while len(roman_value) > 0:
            for index in range(0, len(arrRoman)):
                nLen = len(arrRoman[index])
                if arrRoman[index] == roman_value[0: nLen]:
                  dec += arrDec[index]
                  roman_value = roman_value[nLen: ]
        self.decimal = dec
        return dec

    def convert_to_roman(self):
        arrDec = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
        arrRoman = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V",
            "IV", "I"]
        roman = ""
        decimal_value = self.decimal
        while decimal_value > 0:
            for index in range(0, len(arrDec)):
                if arrDec[index] <= decimal_value:
                    dividend = int(decimal_value / arrDec[index])
                    decimal_value -= dividend * arrDec[index]
                    roman += (arrRoman[index] * dividend)
        return roman

    def check_if_valid(self):
        '''
        Returns true if roman numeral input == roman numeral representation
        from self.convert_to_roman, false otherwise
        '''
        if not self.decimal:
            self.convert_to_decimal()
        check_roman = self.convert_to_roman()
        if check_roman == self.roman:
            return True
        else:
            return False

    def _db_cursor(self, to_do):
        try:
            connection = sqlite3.connect(settings.DB)
            #connection.text_factory = bytes
            if to_do == 'get':
                return connection.cursor()
            if to_do == 'close':
                return connection.close()
        except:
            return 'Error in db_cursor'


    def get_random_movie(self, mov_list):
        #cursor = self._db_cursor('get')
        #if type(cursor) == str:
        #    print(cursor)
        movie_list = mov_list

        #try:
        #    query = 'SELECT tconst, primaryTitle, genres FROM movies WHERE startYear = ?'
        #    cursor.execute(query, (self.decimal, ))
        #except sqlite3.Error as e:
        #    print('Error ', e.args, ' occurred in get_random_movie()')
        #    return (None, 0)
        #movie_list = cursor.fetchall()
        #self._db_cursor('close')

        list_length = len(movie_list)
        random_index = 0
        if list_length > 0:
            random_index = random.randrange(0, list_length)
            return (movie_list[random_index], list_length)
        else:
            return (None, 0)

    def check_for_movies(self):#, year = None):
        #if year:
        #    self.decimal = year
        if self.decimal != None:
            if 1888 <= self.decimal <= 2018:
                return self.get_random_movie()
            else:
                return (None, 0)
        else:
            if 1888 <= self.convert_to_decimal() <= 2018:
                return self.get_random_movie()
            else:
                return (None, 0)

    def get_random_actor(self):
        cursor = self._db_cursor('get')
        if type(cursor) == str:
            print('Error:', cursor)
        actor1 = None
        actor_list = []
        try:
            query = 'SELECT nconst, primaryName, knownForTitles FROM actors WHERE birthYear = ?'
            'SELECT actors.nconst, actors.primaryName, actors.knownForTitles, \
            movies.primaryTitle FROM actors LEFT JOIN movies where \
            movies.tconst IN actors.knownForTitles'
            cursor.execute(query, (self.decimal, ))
            actor_list = cursor.fetchall()
        except sqlite3.Error as e:
            print('Error ', e.args, ' occurred in get_random_movie()')
        list_length = len(actor_list)
        random_index = 0
        if list_length > 0:
            random_index = random.randrange(0, list_length)
            actor1 = list(actor_list[random_index])
            title_IDs = actor1[2].split(',')
            movie_titles = []
            for title_ID in title_IDs:
                try:
                    query = 'select primaryTitle from movies where tconst=?'
                    cursor.execute(query, (title_ID, ))
                    db_listing = cursor.fetchone()
                    if db_listing:
                        movie_titles.append((title_ID, db_listing))
                except:
                    pass
            actor1.append(movie_titles)

        actor2 = None
        actor_list = []
        try:
            query = 'SELECT nconst, primaryName, knownForTitles FROM actors WHERE deathYear = ?'
            cursor.execute(query, (self.decimal, ))
            actor_list = cursor.fetchall()
        except sqlite3.Error as e:
            print('Error ', e.args, ' occurred in get_random_movie()')
        list_length = len(actor_list)
        random_index = 0
        if list_length > 0:
            random_index = random.randrange(0, list_length)
            actor2 = list(actor_list[random_index])
            title_IDs = actor2[2].split(',')
            movie_titles = []
            for title_ID in title_IDs:
                try:
                    query = 'select primaryTitle from movies where tconst=?'
                    cursor.execute(query, (title_ID, ))
                    db_listing = cursor.fetchone()
                    if db_listing:
                        movie_titles.append((title_ID, db_listing))
                except:
                    pass
            actor2.append(movie_titles)
        print(actor1, actor2)
        return (actor1, actor2)

    def get_random_actor2(self, actor_list):
        list_length = len(actor_list)
        random_index = 0
        if list_length > 0:
            random_index = random.randrange(0, list_length)
        return actor_list[random_index]

    def check_for_actors(self):#, year = None):
        if self.decimal != None:
            if 1888 <= self.decimal <= 2018:
                return self.get_random_actor()
            else:
                return (None, 0)
        else:
            if 1888 <= self.convert_to_decimal() <= 2018:
                return self.get_random_actor()
            else:
                return (None, 0)


    def check_for_actors2(self):
        if self.decimal == None:
            self.decimal = self.convert_to_decimal()
        cursor = self._db_cursor('get')
        if type(cursor) == str:
            print(cursor)
        actor_list = []
        try:
            query = 'SELECT nconst, primaryName, knownForTitles FROM actors WHERE birthYear = ?'
            cursor.execute(query, (self.decimal, ))
        except sqlite3.Error as e:
            print('An error (2) occurred in check_for_actors(): ', e.args[0])
        actor_list = cursor.fetchall()
        actor1 = None
        list_length = len(actor_list)
        actor1_title_list = []
        if list_length > 0:
            actor1 = actor_list[random.randrange(0, list_length)]
            title_ids = actor1[2].split(',')
            title = ''
            for title_id in title_ids:
                try:
                    cursor.execute('SELECT primaryTitle FROM movies WHERE isAdult = 0 AND tconst = ?', (title_id, ))
                    title = cursor.fetchone()
                except sqlite3.Error as e:
                    print('An error (3) occurred in check_for_actors(): ', e.args[0])
                if not title == None:
                    actor1_title_list.append([title_id, title[0]])
                if len(actor1_title_list) > 1:
                    break;
        try:
            query = 'SELECT nconst, primaryName, knownForTitles FROM actors WHERE deathYear = ?'
            cursor.execute(query, (self.decimal, ))
        except sqlite3.Error as e:
            print('An error (2) occurred in check_for_actors(): ', e.args[0])
        actor_list = cursor.fetchall()
        actor2 = None
        list_length = len(actor_list)
        actor2_title_list = []
        if list_length > 0:
            actor2 = actor_list[random.randrange(0, list_length)]
            title_ids = actor2[2].split(',')
            for title_id in title_ids:
                try:
                    cursor.execute('SELECT primaryTitle FROM movies WHERE isAdult = 0 AND tconst = ?', (title_id, ))
                    title = cursor.fetchone()
                except sqlite3.Error as e:
                    print('An error (5) occurred in check_for_actors(): ', e.args[0])
                if title != None:
                    actor2_title_list.append([title_id, title[0]])
                if len(actor2_title_list) > 1:
                    break;
        return (actor1, actor2, actor1_title_list, actor2_title_list)

def main():
    print('db path=', settings.DB)
    test_number = Number(1969)
    print(test_number.decimal, ' = ', test_number.convert_to_roman())
    movie_list = ['The Wild Bunch', 'True Grit', 'Erotissimo']
    print('movie data from year ', test_number.decimal, '=', test_number.get_random_movie(movie_list))
    actor_list = ['Jennifer Aniston', 'Judy Garland']
    print('actor data = ', test_number.get_random_actor())
    m = Number('M', 'roman')
    print('check M conversion:', m.decimal)

if __name__ == '__main__':
    main()
