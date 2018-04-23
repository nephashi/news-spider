import common_utils.json_util as ju

class RedisUrlPuller(object):

    def __init__(self, redis_queue_dao):
        self.__redis_queue_dao = redis_queue_dao

    def get_raw_json(self):
        return self.__redis_queue_dao.deque()

    def get_url(self):
        json = self.get_raw_json()
        if (json == None):
            return None
        dic = ju.json2dic(json)
        return dic['link']
