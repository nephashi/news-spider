import common_utils.json_util as ju

class RedisUrlPusher(object):

    def __init__(self, redis_queue_dao, dup_rmv_cache, logger):
        self.__redis_queue_dao = redis_queue_dao
        self.__dup_rmv_cache = dup_rmv_cache
        self.__logger = logger

    def log_cache_status(self):
        status = "url pusher cache status. "
        num_per_level = self.__dup_rmv_cache.get_cache_size_per_level()
        status += "num level: " + str(num_per_level) + "; "
        for i in range(len(num_per_level)):
            status += "in " + str(i) + "th level, num url: " + str(num_per_level[i]) + "; "
        self.__logger.info(status)

    def url_push(self, dic):
        url = dic['link']

        crawled = self.__dup_rmv_cache.if_url_crawled(url)

        if (crawled == False):
            self.__dup_rmv_cache.update_cache(url)
            news_url_json_str = ju.dic2json(dic)
            self.__redis_queue_dao.put(item = news_url_json_str)
            return True
        else:
            return False
