from flask import Flask, render_template, request, redirect, jsonify, url_for
from stats_gen import *
from saver import *


app = Flask(__name__)


@app.route('/', methods=['GET'])
def show_main_page():
    return render_template('mainpage.html')


@app.route('/', methods=['POST'])
def questions():
    new_data = {'language': request.form.get('language').lower(),
                'age': request.form.get('age').lower(),
                'apple': request.form.get('apple').lower(),
                'axe': request.form.get('axe').lower(),
                'horse': request.form.get('horse').lower()}

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
                           aver_age=round(get_average_age(), 1),
                           bar=draw_age_bar())


@app.route('/json')
def all_answers():
    return gen_json()


@app.route('/search', methods=['GET'])
def show_search_page():
    return render_template('search.html')


@app.route('/search', methods=['POST'])
def search():
    search_data = {'words': request.form.get('wordstofind').split(),
                   'minage': int(request.form.get('minage')),
                   'maxage': int(request.form.get('maxage'))}

    try:
        search_results = gen_json(must_contain=search_data['words'],
                                  min_age=search_data['minage'],
                                  max_age=search_data['maxage'])
    except TypeError:
        return '''<p>Что-то пошло не так, попробуйте заново.</p>
               <p><a href="/search">На страницу поиска</a></p>'''

    return redirect(url_for('results', search_results=search_results))


@app.route('/results')
def results():
    search_results = request.args['search_results']
    return render_template('results.html', res=json.loads(search_results))


@app.errorhandler(400)
def bad_request_page(e):
    return '''<p><b>Ошибка 400 Bad Request :(</b></p>
              <p>Скорее всего, вы зачем-то решили перейти на /results руками,
              а не через поиск. Сначала поищите что-нибудь.</p>
              <p><a href="/search">На страницу поиска</a></p>''', 400


if __name__ == '__main__':
    app.run(debug=False)
