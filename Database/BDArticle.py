class DBArticle:
    def __init__(self, header='', plain='', lemma='', url=''):
        self.header = header
        self.plain = plain
        self.lemma = lemma
        self.url = url

    def __str__(self):
        return '{}\n{}\n{}\n{}'.format(self.header, self.plain,
                                       self.lemma, self.url)

    __repr__ = __str__
