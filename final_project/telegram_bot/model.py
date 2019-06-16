from peewee import *


db = SqliteDatabase('anecdotes.db')


class Anecdote(Model):
    text = TextField()
    likes = IntegerField()

    class Meta:
        database = db
