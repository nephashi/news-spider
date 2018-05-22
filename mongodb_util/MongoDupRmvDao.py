from mongoengine import *
from mongodb_util.mongo_entity.DuplicateRemovalCache import DuplicateRemovalCache

class MongoDupRmvDao(object):

    def __init__(self, host, db_name = 'news', port = 27017):
        connect(db_name, host = host, port = port)

    def __mgdbcache2pycache(self, mgdb_cache):
        url_list = []
        for lvl in mgdb_cache.cache:
            url_list.append(list(lvl))
        return url_list

    def save_cache(self, cache_lst):
        mgdb_cache_objs = DuplicateRemovalCache.objects
        for c in mgdb_cache_objs:
            c.delete()
        cache = DuplicateRemovalCache()
        cache['cache'] = cache_lst
        cache.save()

    def query_cache(self):
        mgdb_data = DuplicateRemovalCache.objects
        if (len(mgdb_data) > 0):
            mgdb_cache_obj = DuplicateRemovalCache.objects[0]
            return self.__mgdbcache2pycache(mgdb_cache_obj)
        else:
            return None