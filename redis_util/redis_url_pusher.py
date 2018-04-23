import common_utils.json_util as ju

class RedisUrlPusher(object):

    def __init__(self, redis_queue_dao):
        self.__redis_queue_dao = redis_queue_dao
        # 判断是否重复, 这是一个哈希表数组, 每一个哈希表是一级缓存, 先创建的缓存会被先清理
        self.__crawled_urls = []
        # 判断是否重复的缓存中最多缓存10000条
        self.__crawled_cache_max_size = 10000
        # 使用多级缓存, 最先进入的缓存最先清空
        self.__crawled_cache_level_num = 5

    def url_push(self, dic):
        url = dic['link']

        crawled = False
        for i in range(len(self.__crawled_urls)):
            if (url in self.__crawled_urls[i]):
                crawled = True

        if (crawled == False):
            # 缓存级为空，添加一级缓存
            if (len(self.__crawled_urls) == 0):
                self.__crawled_urls.append({})
            # 缓存级内部溢出，添加一级缓存
            if (len(self.__crawled_urls[-1]) >= self.__crawled_cache_max_size):
                self.__crawled_urls.append({})
            # 缓存级数量达到最大，清除第一级(最早添加的)缓存
            if (len(self.__crawled_urls) == self.__crawled_cache_level_num):
                self.__crawled_urls.pop(0)
                self.__crawled_urls.append({})
            self.__crawled_urls[-1][url] = 1

            news_url_json_str = ju.dic2json(dic)

            self.__redis_queue_dao.put(item = news_url_json_str)

