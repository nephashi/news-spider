from mongoengine import *
from mongoengine.queryset.visitor import Q
from mongodb_util.mongo_entity.News import News
import common_utils.time_util as tu

# 该对象负责新闻对象在mongodb的存取
# 新闻对象以字典的形式与外部进行交互，外部不必关系mongoengine的实体类
class MongoNewsDao(object):

    def __init__(self, host, db_name = 'news', port = 27017):
        connect(db_name, host = host, port = port)

    def __mgnews2pynews(self, mongo_news):
        news_dic = {
            'title': mongo_news.title,
            'link': mongo_news.link,
            'content': mongo_news.content,
            'source': mongo_news.source,
            'date': mongo_news.date,
            'unix_timestamp': mongo_news.unix_timestamp
        }
        return news_dic

    def save_news(self, news_dic):
        news = News()
        for key, value in news_dic.items():
            news[key] = value
        news.save()

    def query_all_news(self):
        rst = []
        mgdb_objs =  News.objects

        for mgdb_obj in mgdb_objs:
            news_dic = self.__mgnews2pynews(mgdb_obj)
            rst.append(news_dic)
        return rst

    def query_news_by_time_interval(self, start_date, end_date):
        if (not tu.is_valid_date(start_date, "%Y-%m-%d") or not tu.is_valid_date(end_date, "%Y-%m-%d")):
            print(str(self.__class__) + ": invalid date format")
            return None

        rst = []
        start_stamp = tu.date2timestamp(start_date)
        end_stamp = tu.date2timestamp(end_date)

        mgdb_objs = News.objects(Q(unix_timestamp__lte=end_stamp) & Q(unix_timestamp__gte=start_stamp))
        for mgdb_obj in mgdb_objs:
            news_dic = self.__mgnews2pynews(mgdb_obj)
            rst.append(news_dic)
        return rst

    def fuzzy_query_news_by_title(self, title):
        rst = []
        mgdb_objs = News.objects(title__contains=title)

        for mgdb_obj in mgdb_objs:
            news_dic = self.__mgnews2pynews(mgdb_obj)
            rst.append(news_dic)
        return rst