from mongoengine import *

class TestEntity(Document):
    name = StringField(default="Mr.Li")