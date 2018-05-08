from mongoengine import *
from datetime import datetime

class News(Document):
    title = StringField(max_length=100, required=True)
    link = StringField(max_length=100)
    content = StringField(required=True)
    source = StringField()
    date = DateTimeField(default=datetime.now(), required=True)
    unix_timestamp = IntField(default=datetime.now(), required=True)
