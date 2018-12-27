import sqlite3
import os


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


def search_by_stemmed(stemmed):
    conn = sqlite3.connect('articles.db')
    c = conn.cursor()
    c.execute('SELECT lemma, url FROM articles WHERE lemma LIKE (?)',
              ('%' + stemmed + '%',))
    results = c.fetchall()
    conn.close()
    return results


def crop_results(tuple_results, stemmed):
    dict_results = {}
    for result in tuple_results:
        index = result[0].find(stemmed)
        dict_results[result[1]] = result[0][index:index+300] + '...'
    return dict_results
