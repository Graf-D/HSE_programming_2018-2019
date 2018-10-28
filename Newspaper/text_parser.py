import re
import urllib.request
from bs4 import BeautifulSoup


def get_paragraphs(link):
    paragraphs = []
    response = urllib.request.urlopen(link)
    html = response.read().decode('utf-8')
    soup = BeautifulSoup(html, 'lxml')
    for art in soup.find_all('article'):
        for paragr in art.find_all('p'):
            for parent in paragr.parents:
                if parent.name == 'form':
                    break
            else:
                paragraphs.append(str(paragr))
    return paragraphs


# modifier
def clean_paragraphs(paragraphs):
    for i in range(len((paragraphs))):
        paragraphs[i] = re.sub('<.*?>', '', paragraphs[i])
        paragraphs[i] = re.sub('\[?\]?', '', paragraphs[i])
    return paragraphs
