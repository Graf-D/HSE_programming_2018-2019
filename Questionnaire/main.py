from flask import Flask, render_template, request, redirect, jsonify
from stats_gen import *
from saver import *


app = Flask(__name__)


@app.route('/', methods=['GET'])
def show_main_page():
    return render_template('mainpage.html')


@app.route('/', methods=['POST'])
def questions():
    new_data = {'language': request.form.get('language'),
                'age': request.form.get('age'),
                'apple': request.form.get('apple'),
                'axe': request.form.get('axe'),
                'horse': request.form.get('horse')}

    try:
        save_to_csv(new_data)
    except TypeError:
        return '''<p>Произошла ошибка, ваш ответ не сохранен.</p>
               <p><a href="/">На главную</a></p>'''

    return redirect('/success')


@app.route('/success')
def success():
    return '''<p>Ваш ответ записан, спасибо!</p>
              <p><a href="/">На главную</a></p>'''


@app.route('/stats')
def stats():
    return render_template('stats.html',
                           lang_usage=sort_languages(),
                           aver_age=round(get_average_age(), 1))


@app.route('/json')
def all_answers():
    return gen_json()


@app.route('/search', methods=['GET'])
def show_search_page():
    return render_template('search.html')


@app.route('/search', methods=['POST'])
def search():
    search_data = {'words': request.form.get('wordstofind').split(),
                   'minage': request.form.get('minage'),
                   'maxage': request.form.get('maxage')}

    try:
        json_ = gen_json(must_contain=search_data['words'],
                         min_age=search_data['minage'],
                         max_age=search_data['maxage'])
    except TypeError:
        return '''<p>Что-то пошло не так, попробуйте заново.</p>
               <p><a href="/search">На страницу поиска</a></p>'''

    return redirect('/results')


@app.route('/results')
def results():
    return render_template('results.html')


if __name__ == '__main__':
    app.run(debug=False)
