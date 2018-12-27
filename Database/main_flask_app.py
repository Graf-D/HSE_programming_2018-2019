from flask import Flask, render_template, request
from db_search import *


app = Flask(__name__)


@app.route('/', methods=['GET'])
def search():
    search_line = request.args.get('tofind')
    if not search_line:
        return render_template('search.html', res=[])

    stemmed_request = stem_request(search_line)
    results = crop_results(search_by_stemmed(stemmed_request), stemmed_request)
    return render_template('search.html', res=results, search_line=search_line)


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
