from redis_util.redis_queue_dao import RedisQueueDao
from redis_util.redis_url_puller import RedisUrlPuller
from mongodb_util.MongoNewsDao import MongoNewsDao
from scrapy.exceptions import DropItem

class NewsPipeline(object):

    def __init__(self, redis_uri, redis_password, mgdb_uri, redis_port = 6379, redis_queue_key = "queue",
                       mgdb_port = 27017, mgdb_db_name = 'news_db'):
        self.__redis_uri = redis_uri
        self.__redis_password = redis_password
        self.__redis_port = redis_port
        self.__redis_queue_key = redis_queue_key

        self.__mgdb_uri = mgdb_uri
        self.__mgdb_port = mgdb_port
        self.__mgdb_db_name = mgdb_db_name

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            redis_uri=crawler.settings.get('REDIS_URI'),
            redis_password=crawler.settings.get('REDIS_PASSWORD'),
            redis_port=int(crawler.settings.get('REDIS_PORT')),
            redis_queue_key=crawler.settings.get('REDIS_QUEUE_KEY'),
            mgdb_uri=crawler.settings.get('MGDB_URI'),
            mgdb_port=int(crawler.settings.get('MGDB_PORT')),
            mgdb_db_name=crawler.settings.get('MGDB_DB_NAME')
        )

    def open_spider(self, spider):
        rqd = RedisQueueDao(host = self.__redis_uri,
                            password = self.__redis_password,
                            port = self.__redis_port,
                            queue_key = self.__redis_queue_key)
        self.__rup = RedisUrlPuller(rqd)
        spider.set_redis_puller(self.__rup)

        self.__mnd = MongoNewsDao(host=self.__mgdb_uri,
                                  port=self.__mgdb_port,
                                  db_name=self.__mgdb_db_name)

    def close_spider(self, spider):
        del self.__rup
        del self.__mnd

    def process_item(self, item, spider):
        if (len(item['content']) < 50):
            spider.logger.info("news droped since too short content.")
            raise DropItem("news droped since too short content.")
        if (item['title'] == None or len(item['title']) == 0):
            raise DropItem("news droped since empty title.")

        self.__mnd.save_news(item)
        spider.logger.info("save in mongodb: " + item['title'])