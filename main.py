#python3
from flask import Flask, render_template, request, url_for
from datetime import date
import number

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    start_type = request.form['numType']
    start_value = request.form['startValue']
    user_number = number.Number(start_value, start_type)
    end_value = ''
    is_roman_valid = None
    check_dec_to_roman = None
    if start_type == 'decimal':
        end_value = user_number.convert_to_roman()
    else:
        end_value = user_number.convert_to_decimal()
        is_roman_valid = user_number.check_if_valid()
        check_dec_to_roman = user_number.convert_to_roman()
        print('is valid roman numeral = ', is_roman_valid)
    movie = []
    movie_info, movies_that_year = user_number.check_for_movies()
    (actor1, actor2, actor1_title_list,
        actor2_title_list) = user_number.check_for_actors()
    print('movieInfo=', movie_info)
    print('actorInfo=', actor1, actor2, actor1_title_list, actor2_title_list)
    #this_year = year(today())
    return render_template('result.html', startValue = start_value,
            endValue = end_value, is_roman_valid = is_roman_valid,
            check_dec_to_roman = check_dec_to_roman, movie = movie_info,
            movieCount = movies_that_year, actor1 = actor1,
            actor1Titles = actor1_title_list, actor2 = actor2,
            actor2Titles = actor2_title_list, thisYear = date.today().year)

def main():
    dec_num = Number(1950)
    roman_num = Number("MXXXIX", "roman")
    print("roman=", dec_num.convert_to_roman())
    print("cTD=", roman_num.convert_to_decimal())

if __name__ == '__main__':
    #app.run(debug = False)
    app.run(debug = True)
