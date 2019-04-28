from math import ceil
from flask import Flask, render_template, request
from db_search import *


app = Flask(__name__)


@app.route('/', methods=['GET'])
def search():
    search_line = request.args.get('tofind')
    if not search_line:
        return render_template('search.html', res={}, page=0, maxpages=0)

    page = int(request.args.get('page', 0))

    stemmed_request = stem_request(search_line)
    maxpages = ceil(count_results(stemmed_request) // PAGE_SIZE)
    results = convert_results(search_by_stemmed(stemmed_request, page),
                              stemmed_request)

    return render_template('search.html', res=results, search_line=search_line,
                           page=page, maxpages=maxpages)


if __name__ == '__main__':
    try:
        app.run(debug=False)
    finally:
        close_db()
