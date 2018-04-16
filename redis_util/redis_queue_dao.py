import redis

class RedisQueueDao(object):

    def __init__(self, host, password, port = 6379, decode_responses = True, queue_key = "queue"):
        self.__db = redis.StrictRedis(host = host, password = password, port = port, decode_responses = decode_responses)
        self.__host = host
        self.__password = password
        self.__port = port
        self.__key = queue_key

    def qsize(self):
        return self.__db.llen(self.__key)

    def put(self, item):
        self.__db.rpush(self.__key, item)

    def deque_block(self, timeout = None):
        item = self.__db.blpop(self.__key, timeout = timeout)
        return item

    def deque(self):
        item = self.__db.lpop(self.__key)
        return item

    def get_all(self):
        lst = self.__db.lrange(self.__key, 0, -1)
        return lst

if __name__ == "__main__":
    rqd = RedisQueueDao(host = '13.231.182.153', password = 'redisredis')
    ans = rqd.deque()
    print(ans)