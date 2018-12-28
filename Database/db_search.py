import sqlite3
import os
from threading import local

from Article import Article
from SearchResult import SearchResult


PAGE_SIZE = 20
LOCAL_STORAGE = local()


def get_db(db_name='articles.db'):
    if not hasattr(LOCAL_STORAGE, '_db'):
        LOCAL_STORAGE._db = sqlite3.connect(db_name)
    return LOCAL_STORAGE._db


def close_db():
    get_db().close()


def stem_request(request_text):
    with open('temp.txt', 'w', encoding='utf-8') as f:
        print(request_text, file=f)

    this_dir = os.path.dirname(os.path.abspath(__file__))
    source = this_dir + '\\' + 'temp.txt'
    save_to = os.path.join(this_dir, 'stemmed.txt')

    os.system(' '.join(['C:\mystem.exe', source, save_to,
              '-i', '-l', '-c', '-d', '--eng-gr']))

    with open('stemmed.txt', 'r', encoding='utf-8') as f:
        stemmed = f.read()
    os.remove('temp.txt')
    os.remove('stemmed.txt')

    return stemmed.strip('\n')


def count_results(stemmed):
    c = get_db().cursor()
    c.execute('SELECT COUNT(*) FROM articles WHERE lemma LIKE (?)',
              ('%' + stemmed + '%',))
    return c.fetchone()[0]


def search_by_stemmed(stemmed, page):
    c = get_db().cursor()
    # * doesn't guarantee an order of columns
    # source: https://www.sqlite.org/lang_select.html
    c.execute('SELECT header, plain, lemma, url FROM articles'
              ' WHERE lemma LIME (?) LIMIT (?) OFFSET (?)',
              ('%' + stemmed + '%', PAGE_SIZE, page * PAGE_SIZE))
    results = c.fetchall()

    articles = []
    for result in results:
        articles.append(Article(*result))

    return articles


def convert_results(articles, stemmed):
    return [SearchResult(article, stemmed) for article in articles]
