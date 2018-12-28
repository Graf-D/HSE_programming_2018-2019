import re
from functools import lru_cache


class SearchResult:
    def __init__(self, article, stemmed):
        self.article = article
        self.stemmed = stemmed

    @property
    @lru_cache()
    def lemma_index(self):
        return self.article.lemma.find(self.stemmed)

    @property
    def lemma_summary(self):
        if self.lemma_index >= 100:
            start = self.lemma_index - 100
        else:
            start = self.lemma_index
        return self.article.lemma[start:self.lemma_index + 300] + '...'

    def find_plain(self):
        # there were some issues with \t \n etc
        onlyspaces_lemma = re.sub(r'\s', ' ', self.article.lemma)
        slice_end = onlyspaces_lemma.find(self.stemmed)
        cropped_lemma = onlyspaces_lemma[:slice_end]
        # word's position in text equals to number of spaces before it
        word_num = cropped_lemma.count(' ')
        return word_num

    @property
    def plain_summary(self):
        word_num = self.find_plain()
        # if there are less than 10 words in left context
        # they all would be shown
        # else there would be only 10 words
        left = max(word_num - 20, 0)
        right = left + 50
        onlyspaces_plain = re.sub(r'\s', ' ', self.article.plain)
        return ' '.join(onlyspaces_plain.split()[left:right])
