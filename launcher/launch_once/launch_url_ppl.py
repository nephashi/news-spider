import sys
import platform

if __name__ == '__main__':
    # import模块必备
    def add_proj_path_to_syspath():
        sp = get_spliter()
        proj_path = sp.join(sys.path[0].split(sp)[0:-2])
        sys.path.append(proj_path)
        print('add project path: ' + proj_path + ' to system path')

    def get_spliter():
        if platform.system() == "Windows":
            return '\\'
        else:
            return '/'

    add_proj_path_to_syspath()

from scrapy.crawler import CrawlerProcess
sys.stderr = sys.stdout

def launch_crawl_single_homepage_for_url(spider_cls, log_path):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'ITEM_PIPELINES': '{"pipeline.UrlPushPipeline.UrlPushPipeline": 300}',
        'DOWNLOAD_DELAY': '600',
        'REDIS_URI': '13.231.182.153',
        'REDIS_PASSWORD': 'redisredis',
        'REDIS_PORT': '6379',
        'REDIS_QUEUE_KEY': 'queue_test',
        'CACHE_MGDB_URI': '18.182.13.109',
        'CACHE_MGDB_PORT': '27017',
        'CACHE_MGDB_DB_NAME': 'news_db_test',
        'NUM_CACHE_LVL': '5',
        'CACHE_MAX_SIZE': '10000',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'LOG_FILE': log_path,
        'LOG_ENCODING': 'utf-8'
    })
    process.crawl(spider_cls)
    process.start()
    print("url spider finished: " + str(spider_cls))

upper_module_name = 'spider.url_spider'
spider_name = sys.argv[1]
module_name = upper_module_name + '.' + spider_name
m = __import__(module_name, fromlist=True)
spider_cls = getattr(m, spider_name)
log_path = sys.argv[2]

launch_crawl_single_homepage_for_url(spider_cls, log_path)