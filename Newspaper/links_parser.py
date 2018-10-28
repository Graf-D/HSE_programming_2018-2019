import re
import urllib.request
from bs4 import BeautifulSoup
from conf import *
from Article import Article


def get_headers_and_topics(soup, headers=[], topics=[]):
    for header in soup.find_all('h3'):
        header = str(header)
        if 'href' in header:  # there are h3 which are not news
            headers.append(header)
            curr_topic = ''
            for key, value in TOPICS.items():
                if value in header:
                    curr_topic = key
            if curr_topic:
                topics.append(curr_topic)
            else:
                topics.append(None)
    return headers, topics


def get_authors(soup):
    authors = []
    counter = 0
    for tag in soup.find_all('dd'):
        if 'createdby' in str(tag):
            authors.append(str(tag)[len('<dd class="createdby"> Автор: '):-6])
            counter += 1
    if counter < len(soup.find_all('dd')) / 2:
        authors.append(None)
    return authors


def get_dates(soup):
    dates = []
    for tag in soup.find_all('dd'):
        if 'published' in str(tag):
            dates.append(re.search('\d{2}\.\d{2}\.\d{4}', str(tag)).group())
    return dates


# modifier
def make_headers_and_links(headers, links):
    for i in range(len(headers)):
        header = headers[i]
        links.append(BASE_URL +
                     header[len('<h3> <a href="'):header.index('">')])
        headers[i] = header[header.index('"> ') + 3:header.index('</a>')]
    return headers, links


def get_articles():
    articles = []

    links = []
    headers = []
    topics = []
    authors = []
    dates = []

    for i in range(0, 4032, 29):
        curr_url = BASE_URL + '/?start=' + str(i)
        response = urllib.request.urlopen(curr_url)
        html = response.read().decode('utf-8')
        soup = BeautifulSoup(html, 'lxml')

        headers, topics = get_headers_and_topics(soup, headers, topics)
        authors += get_authors(soup)
        dates += get_dates(soup)

    # modifier
    headers, links = make_headers_and_links(headers, links)

    for i, link in enumerate(links):
        try:
            articles.append(Article(link, headers[i],
                                    topics[i], authors[i], dates[i]))
        except:
            print('i:', i, 'link:', link, 'end of the link')
            print(headers[i])
            print(len(headers), len(topics), len(authors), len(dates))
            print(authors[i-1])
            __import__('sys').stdout.flush()

    return articles
