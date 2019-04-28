import vk
import time
from datetime import datetime
from functools import lru_cache

import nltk
from nltk.corpus import stopwords
from pymystem3 import Mystem
from string import punctuation

from conf import *
from comment import Comment


class Post:
    def __init__(self, id_, date, text):
        self.id_ = id_
        self.date = date
        self.text = text

        self.vk_api = vk.API(vk.Session(access_token=ACCESS_TOKEN))
        self.mystem = Mystem()
        self.stopwords = stopwords.words('russian')

    @property
    def month(self):
        return datetime.utcfromtimestamp(self.date).month

    @property
    def weekday(self):
        return datetime.utcfromtimestamp(self.date).weekday()

    @property
    @lru_cache()
    def comments(self):
        response = self.vk_api.wall.getComments(owner_id=OWNER_ID, v=VERSION,
                                                post_id=self.id_, count=100)
        time.sleep(0.35)
        raw_comments = response['items']

        if response['count'] > 100:
            for i in range(response['count'] // 100 + 1):
                new_comments = self.vk_api.wall.getComments(owner_id=OWNER_ID,
                                                            v=VERSION,
                                                            post_id=self.id_,
                                                            count=100,
                                                            offset=100*(i+1))
                raw_comments += new_comments['items']
                time.sleep(0.35)

        comments = []
        for item in raw_comments:
            if not item.get('deleted', False):
                comments.append(Comment(self, item['id'],
                                        item['from_id'], item['text']))

        return comments

    @property
    def lemmatized_text(self):
        tokens = self.mystem.lemmatize(self.text.lower())
        tokens = [token for token in tokens if (token.strip() and
                                                token not in punctuation)]
        lemmatized_text = ' '.join(tokens)
        return lemmatized_text
