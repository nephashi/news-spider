from mongodb_util import MongoDupRmvDao

class DuplicateRemovalCache(object):

    def __init__(self, mdr_dao, cache_max_size, num_cache_level):
        self.__mongo_dup_rmv_dao = mdr_dao
        # 判断是否重复, 这是一个哈希表数组, 每一个哈希表是一级缓存, 先创建的缓存会被先清理
        self.__crawled_url_cache = []
        # 判断是否重复的缓存中最多缓存多少条
        self.__crawled_cache_max_size = cache_max_size
        # 使用多级缓存, 最先进入的缓存最先清空
        self.__num_crawled_cache_level = num_cache_level

    def load_url_cache(self):
        db_cache = self.__mongo_dup_rmv_dao.query_cache()
        if (db_cache != None):
            self.__crawled_url_cache = []
            for inner_lst in db_cache:
                cur_lvl = {}
                for url in inner_lst:
                    cur_lvl[url] = 1
                self.__crawled_url_cache.append(cur_lvl)
        else:
            self.__crawled_url_cache = []

    def save_url_cache(self):
        url_lst = []
        for dic in self.__crawled_url_cache:
            url_lst.append(list(dic.keys()))
        self.__mongo_dup_rmv_dao.save_cache(url_lst)

    def if_url_crawled(self, url):
        crawled = False
        for i in range(len(self.__crawled_url_cache)):
            if (url in self.__crawled_url_cache[i]):
                crawled = True
                break
        return crawled

    def update_cache(self, uncrawled_url):
        # 缓存级为空，添加一级缓存
        if (len(self.__crawled_url_cache) == 0):
            self.__crawled_url_cache.append({})
        # 缓存级内部溢出，添加一级缓存
        if (len(self.__crawled_url_cache[-1]) >= self.__crawled_cache_max_size):
            self.__crawled_url_cache.append({})
        # 缓存级数量达到最大，清除第一级(最早添加的)缓存
        if (len(self.__crawled_url_cache) > self.__num_crawled_cache_level):
            self.__crawled_url_cache.pop(0)
        self.__crawled_url_cache[-1][uncrawled_url] = 1

    # 返回一个整数表，内容是各个缓存级的长度
    def get_cache_size_per_level(self):
        ans = []
        for c in self.__crawled_url_cache:
            ans.append(len(c.items()))