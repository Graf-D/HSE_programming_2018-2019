from peewee import *

from posts_fetcher import posts


db = SqliteDatabase('anecdotes.db')


class Anecdote(Model):
    text = TextField()
    likes = IntegerField()

    class Meta:
        database = db


db.create_tables([Anecdote])

for post in posts:
    anecdote = Anecdote.create(text=post.text, likes=post.likes)
    anecdote.save()

db.close()
