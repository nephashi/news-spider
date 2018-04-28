from mongoengine import *
from mongodb_util.mongo_entity.TestEntity import TestEntity

print("connecting")
connect('test', host = '18.182.13.109')


t = TestEntity()
t['name'] = 'jerry'
print("saving")
t.save()
print("end")

# ts = TestEntity.objects
#
# print(ts)