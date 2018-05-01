import common_utils.json_util as ju

# 拉到链接数据后，会在该对象内缓存，随时可以取到
class RedisUrlPuller(object):

    def __init__(self, redis_queue_dao):
        self.__redis_queue_dao = redis_queue_dao
        self.__last_pulled_item = None

    def get_raw_json(self):
        return self.__redis_queue_dao.deque()

    def get_url(self):
        json = self.get_raw_json()
        if (json == None):
            return None
        dic = ju.json2dic(json)
        self.__last_pulled_item = dic
        return dic['link']

    def get_last_pulled_item(self):
        return self.__last_pulled_item
