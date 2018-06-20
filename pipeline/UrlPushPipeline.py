import common_utils.check as check
from scrapy.exceptions import DropItem
from redis_util.redis_queue_dao import RedisQueueDao
from redis_util.redis_url_pusher import RedisUrlPusher
from mongodb_util.MongoDupRmvDao import MongoDupRmvDao
from redis_util.duplicate_removal_cache import DuplicateRemovalCache

class UrlPushPipeline(object):

    def __init__(self, redis_uri, redis_password, mgdb_uri, num_cache_lvl, cache_max_size, redis_port = 6379, redis_queue_key = "queue",
                       mgdb_port=27017, mgdb_db_name='news_db'):
        self.__redis_uri = redis_uri
        self.__redis_password = redis_password
        self.__redis_port = redis_port
        self.__redis_queue_key = redis_queue_key

        self.__mgdb_uri = mgdb_uri
        self.__mgdb_port = mgdb_port
        self.__mgdb_db_name = mgdb_db_name
        self.__num_cache_lvl = num_cache_lvl
        self.__cache_max_size = cache_max_size

        # RedisUrlPusher
        self.__rup = None

        self.__url_count = 0
        self.__redis_push_count = 0
        self.__cache_update_counter = 0

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            redis_uri = crawler.settings.get('REDIS_URI'),
            redis_password = crawler.settings.get('REDIS_PASSWORD'),
            redis_port = int(crawler.settings.get('REDIS_PORT')),
            redis_queue_key = crawler.settings.get('REDIS_QUEUE_KEY'),

            mgdb_uri = crawler.settings.get('CACHE_MGDB_URI'),
            mgdb_port = int(crawler.settings.get('CACHE_MGDB_PORT')),
            mgdb_db_name = crawler.settings.get('CACHE_MGDB_DB_NAME'),

            num_cache_lvl = int(crawler.settings.get('NUM_CACHE_LVL')),
            cache_max_size = int(crawler.settings.get('CACHE_MAX_SIZE'))
        )

    def open_spider(self, spider):
        rqd = RedisQueueDao(host = self.__redis_uri,
                            password = self.__redis_password,
                            port = self.__redis_port,
                            queue_key = self.__redis_queue_key)
        mdrd = MongoDupRmvDao(host = self.__mgdb_uri,
                              db_name = self.__mgdb_db_name,
                              port = self.__mgdb_port)
        self.__drc = DuplicateRemovalCache(mdrd, self.__cache_max_size, self.__num_cache_lvl)
        self.__drc.load_url_cache()
        self.__rup = RedisUrlPusher(rqd, self.__drc, spider.logger)

    def close_spider(self, spider):
        self.__drc.save_url_cache()
        del self.__drc
        del self.__rup

    def process_item(self, item, spider):
        link_url = item['link']
        if (not check.checkLink(link_url)):
            raise DropItem("Invalid link, drop item.")
        else:
            if_push = self.__rup.url_push(item)
            if (if_push == True):
                spider.logger.info("push to redis")
                self.__redis_push_count += 1
            else:
                spider.logger.info("duplicate item")
            self.__url_count += 1
            self.__cache_update_counter += 1

            if (self.__cache_update_counter == 300):
                self.__drc.save_url_cache()
                self.__cache_update_counter = 0
            return item
