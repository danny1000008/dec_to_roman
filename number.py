import pymysql
import os.path
from random import randrange

class Number():
    """docstring for ."""
    def __init__(self, num, num_type = 'decimal'):
        self.decimal = None
        self.roman = None
        self.number_movies = None
        self.movie = None
        if num_type == "roman" and type(num) == str:
            self.roman = num
        else: # num_type == 'decimal':
            self.decimal = int(num)

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

    def get_random_movie(self):
        is_in_range = True
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        #db_path = os.path.join(BASE_DIR, 'static\movieInfo.db')
        db_path = os.path.join(BASE_DIR, 'static\moviesSmall.db')
        my_db_host = 'mysql.dannywagstaff.com'
        user_name = 'dwagstaff24'
        password = 'DHB1rdie!'
        db = 'moviessmall'
        connection = pymysql.connect(host = my_db_host, user = user_name,
            passwd = password, db = db)
        cursor = connection.cursor()
        #query = 'SELECT tconst, primaryTitle, genres FROM moviesSmall WHERE \
        #    isAdult = "0" AND titleType = "movie" '
        query = 'SELECT tconst, primaryTitle, genres FROM moviesSmall WHERE \
            isAdult = "0" AND titleType = "movie" AND startYear = %s'
        movie_list = []
        print(query)
        try:
            #cursor.execute(query + 'AND startYear = ?', (str(self.decimal), ))
            cursor.execute(query, [str(self.decimal)])
            movie_list = cursor.fetchall()
        except pymysql.Error as e:
            print('An error (1) occurred in get_random_movie(): ', e.args[0])
        connection.close()
        list_length = len(movie_list)
        random_index = 0
        if list_length > 0:
            random_index = randrange(0, list_length)
            return movie_list[random_index], list_length
        else:
            return None, 0

    def check_for_movies(self, year = None):
        if year:
            self.decimal = year
        if self.decimal != None:
            if 1888 <= self.decimal <= 2018:
                return self.get_random_movie()
            else:
                return None, None
        else:
            if 1888 <= self.convert_to_decimal() <= 2018:
                return self.get_random_movie()
            else:
                return None, None

    def get_random_actor(self, actor_list):
        is_in_range = True
        list_length = len(actor_list)
        random_index = 0
        if list_length > 0:
            random_index = randrange(0, list_length)
        return actor_list[random_index]

    def check_for_actors(self):
        if self.decimal == None:
            self.decimal = self.convert_to_decimal()
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        #db_path = os.path.join(BASE_DIR, 'static\movieInfo.db')
        db_path = os.path.join(BASE_DIR, 'static\moviesSmall.db')
        my_db_host = 'mysql.dannywagstaff.com'
        user_name = 'dwagstaff24'
        password = 'DHB1rdie!'
        db = 'moviessmall'
        connection = pymysql.connect(host = my_db_host, user = user_name,
            passwd = password, db = db)
        cursor = connection.cursor()
        actor_list = []
        try:
            #cursor.execute('SELECT nconst, primaryName, knownForTitles FROM data_actors WHERE birthYear = ?', (str(self.decimal), ))
            cursor.execute('SELECT nconst, primaryName, knownForTitles FROM actorsSmall WHERE birthYear = %s', [str(self.decimal)])
            actor_list = cursor.fetchall()
        except pymysql.Error as e:
            print('An error (2) occurred in check_for_actors(): ', e.args[0])
        actor1 = None
        list_length = len(actor_list)
        actor1_title_list = []
        if list_length > 0:
            actor1 = actor_list[randrange(0, list_length)]
            title_ids = actor1[2].split(',')
            #actor1[2] = []
            for title_id in title_ids:
                try:
                    #cursor.execute('SELECT title FROM titleIds WHERE region = "US" AND titleId = ?', (title_id, ))
                    cursor.execute('SELECT primaryTitle FROM moviesSmall WHERE isAdult = 0 AND tconst = %s', [title_id])
                    title = cursor.fetchone()
                except pymysql.Error as e:
                    print('An error (3) occurred in check_for_actors(): ', e.args[0])
                #print('titleId1=', title_id)
                if title != None:
                    actor1_title_list.append([title_id, title[0]])
                    #actor1_title_list.append(title_id)
                    #actor1[2].append(title)
                if len(actor1_title_list) > 1:
                    break;
        actor_list = []
        try:
            #cursor.execute('SELECT nconst, primaryName, knownForTitles FROM data_actors WHERE deathYear = ?', (str(self.decimal), ))
            #cursor.execute('SELECT nconst, primaryName, knownForTitles FROM actorsSmall WHERE deathYear = ?', (str(self.decimal), ))
            cursor.execute('SELECT nconst, primaryName, knownForTitles FROM actorsSmall WHERE deathYear = %s', [str(self.decimal)])
            actor_list = cursor.fetchall()
        except pymysql.Error as e:
            print('An error (4) occurred in check_for_actors(): ', e.args[0])
        actor2 = None
        list_length = len(actor_list)
        actor2_title_list = []
        if list_length > 0:
            actor2 = actor_list[randrange(0, list_length)]
            #print('titleIds, type=', actor2[1], type(actor2[1]))
            title_ids = actor2[2].split(',')
            for title_id in title_ids:
                try:
                    #cursor.execute('SELECT title FROM titleIds WHERE region = "US" AND titleId = ?', (title_id, ))
                    cursor.execute('SELECT primaryTitle FROM moviesSmall WHERE isAdult = 0 AND tconst = %s', [title_id])
                    title = cursor.fetchone()
                except pymysql.Error as e:
                    print('An error (5) occurred in check_for_actors(): ', e.args[0])
                if title != None:
                    actor2_title_list.append([title_id, title[0]])
                    #actor2_title_list.append(title_id)
                if len(actor2_title_list) > 1:
                    break;
        connection.close()
        return (actor1, actor2, actor1_title_list, actor2_title_list)

def main():
    test_number = Number(1980)
    print(test_number.decimal, ' = ', test_number.convert_to_roman())
    year = 1999
    print('movie data from year ', year, '=', test_number.check_for_movies(year))
    print('actor data = ', test_number.check_for_actors())

if __name__ == '__main__':
    main()
