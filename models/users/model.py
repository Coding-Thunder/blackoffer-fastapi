import profile
from mongoengine import Document, StringField, IntField, ListField


class Users(Document):
    username = StringField(max_length=100)
    password = StringField()
