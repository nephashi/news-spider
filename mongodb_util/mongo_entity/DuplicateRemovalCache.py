from mongoengine import *

class DuplicateRemovalCache(Document):
    cache = ListField(DictField)
