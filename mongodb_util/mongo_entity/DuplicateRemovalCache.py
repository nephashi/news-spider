from mongoengine import *

class DuplicateRemovalCache(Document):
    cache = ListField(ListField(StringField()))
