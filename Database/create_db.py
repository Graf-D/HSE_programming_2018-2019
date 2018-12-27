import sqlite3
import os
from DBArticle import DBArticle


conn = sqlite3.connect('articles.db')
c = conn.cursor()
c.execute("CREATE TABLE IF NOT EXISTS articles"
          "(header text, plain text, lemma text, url text)")

articles = []
for root, dirs, files in os.walk('plain'):
    if not dirs:
        for file in files:
            if 'onlytext' in file:
                with open(root + '\\' + file, 'r', encoding='utf-8') as f:
                    this_plain = f.read()

                path = root + '\\' + file[8:]
                with open(path, 'r', encoding='utf-8') as f:
                    for line in f.readlines():
                        if '@ti' in line:
                            this_header = line[4:].strip('\n')
                        elif '@url' in line:
                            this_url = line[5:].strip('\n')

                path = root.replace('plain', 'mystem-plain') + '\\' + file[9:]
                with open(path, 'r', encoding='utf-8') as f:
                    this_lemma = f.read()

                articles.append(DBArticle(this_header, this_plain,
                                          this_lemma, this_url))


for article in articles:
    header = article.header
    plain = article.plain
    lemma = article.lemma
    url = article.url
    c.execute("INSERT INTO articles VALUES "
              "(?, ?, ?, ?)", (header, plain, lemma, url))
    conn.commit()

conn.close()
