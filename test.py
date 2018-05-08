# from mongodb_util.MongoNewsDao import MongoNewsDao
#
# mnd = MongoNewsDao('18.182.13.109', 'news_db')
# aus_news = mnd.fuzzy_query_news_by_title('五一')
#
# print('done')

# from mongoengine import *
# from mongodb_util.mongo_entity.News import News
#
# print('connecting')
# connect('news_db', host='18.182.13.109', port=27017)
# connect('test', host='18.182.13.109', port=27017)
# print('querying')
# mgdb_objs =  News.objects(title__contains='中国')
# print(len(mgdb_objs))
#
# print("end")

from mongoengine import *

class DuplicateRemovalCache(Document):
    cache = ListField(DictField)