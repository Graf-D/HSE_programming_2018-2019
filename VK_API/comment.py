import vk
import re
import time
from functools import lru_cache
from pymystem3 import Mystem
from string import punctuation

from conf import *
from user import User


class Comment:
    def __init__(self, post, id_, author_id, text):
        self.post = post
        self.id_ = id_
        self.text = text
        self.author_id = author_id

        self.vk_api = self.post.vk_api
        self.mystem = self.post.mystem

    @property
    def num_of_words(self):
        splitted = re.split('\W+', self.text)
        return len([elem for elem in splitted if elem != ''])

    @property
    @lru_cache()
    def author(self):
        author_info = self.vk_api.users.get(user_ids=self.author_id,
                                            fields=['sex', 'has_photo'],
                                            v=VERSION)
        time.sleep(0.35)
        return User(author_info[0]['id'], author_info[0]['sex'],
                    author_info[0]['has_photo'])

    @property
    def lemmatized_text(self):
        tokens = self.mystem.lemmatize(self.text.lower())
        tokens = [token for token in tokens if (token.strip() and
                                                token not in punctuation)]
        lemmatized_text = ' '.join(tokens)
        return lemmatized_text
