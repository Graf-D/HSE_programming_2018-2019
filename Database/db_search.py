import sqlite3
import os
from threading import local


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
    c.execute('SELECT header, lemma, url FROM articles WHERE lemma LIKE (?)'
              ' LIMIT (?) OFFSET (?)',
              ('%' + stemmed + '%', PAGE_SIZE, page * PAGE_SIZE))
    results = c.fetchall()
    return results


def crop_results(tuple_results, stemmed):
    dict_results = {}
    for result in tuple_results:
        index = result[1].find(stemmed)
        if index >= 100:
            start = index - 100
        else:
            start = index
        dict_results[result[2]] = [result[0],
                                   result[1][start:index+300] + '...']
    return dict_results
