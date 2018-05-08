import sys
import platform

# import模块必备
def add_proj_path_to_syspath():
    sp = get_spliter()
    proj_path = sp.join(sys.path[0].split(sp)[0:-1])
    sys.path.append(proj_path)
    print('add project path: ' + proj_path + ' to system path')

def get_spliter():
    if platform.system() == "Windows":
        return '\\'
    else:
        return '/'

add_proj_path_to_syspath()

from scrapy.crawler import CrawlerProcess
from spider.url_spider.SinaHomeSpider import SinaHomeSpider

sys.stderr = sys.stdout

def launch_crawl_single_homepage_for_url(spider_cls):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'ITEM_PIPELINES': '{"pipeline.UrlPushPipeline.UrlPushPipeline": 300}',
        'DOWNLOAD_DELAY': '600',
        'REDIS_URI': '13.231.182.153',
        'REDIS_PASSWORD': 'redisredis',
        'REDIS_PORT': '6379',
        'REDIS_QUEUE_KEY': 'queue',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'LOG_FILE': '../logs/URLSpider.log',
        'LOG_ENCODING': 'utf-8'
    })
    process.crawl(spider_cls)
    process.start()
    print("url spider finished: " + str(SinaHomeSpider))

launch_crawl_single_homepage_for_url(SinaHomeSpider)