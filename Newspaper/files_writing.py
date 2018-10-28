import Article
import os
import re
import hashlib
import datetime


def to_datetime_date(str_date):
    day, month, year = list(map(int, str_date.split('.')))
    return datetime.date(year, month, day)


def make_dataframe_dict(path, author, header, date, topic, link):
    d = {'path': path,
         'author': author,
         'header': header,
         'created': date,
         'sphere': 'публицистика',
         'topic': topic,
         'style': 'нейтральный',
         'audience_age': 'н-возраст',
         'audience_level': 'н-уровень',
         'audience_size': 'городская',
         'source': link,
         'publication': 'Открытая Дубна',
         'publ_year': to_datetime_date(date).year,
         'medium': 'газета',
         'country': 'Россия',
         'region': 'город Дубна, Московская область',
         'language': 'ru'}
    return d


def gen_file_path(article):
    this_date = to_datetime_date(article.date)
    this_path = ('plain' + '/' +
                 str(this_date.year) + '/' +
                 str(this_date.month) + '/' +
                 str(this_date.day))

    if not os.path.exists(this_path):
        os.makedirs(this_path)

    filename_hash = hashlib.md5(article.header.encode()).hexdigest() + '.txt'
    file_path = (this_path + '/' +
                 re.sub('[\\\/:\*\?"<>|]', '', filename_hash))
    return file_path


def article_to_file(article, file_path):
    with open(file_path, 'w', encoding='utf-8') as f:
        print('@au', article.author, file=f)
        print('@ti', article.header, file=f)
        print('@da', article.date, file=f)
        print('@topic', article.topic, file=f)
        print('@url', article.link, file=f)
        print('\n'.join(article.text), file=f)
