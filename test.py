from scrapy.crawler import CrawlerProcess
from spider.url_spider.TencentModuleSpider import TencentModuleSpider
from spider.url_spider.SinaHomeSpider import SinaHomeSpider
from spider.url_spider.TencentHomeSpider import TencentHomeSpider

process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'DOWNLOADER_MIDDLEWARES': '{"middleware.FailureMiddleware.FailureMiddleware": 0}',
        'DOWNLOAD_DELAY': '1',
        'REDIS_URI': '13.231.182.153',
        'REDIS_PASSWORD': 'redisredis',
        'REDIS_PORT': '6379',
        'REDIS_QUEUE_KEY': 'queue_test',
        'MGDB_URI': '18.182.13.109',
        'MGDB_PORT': '27017',
        'MGDB_DB_NAME': 'news_db_test',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'LOG_FILE': './LOG',
        'LOG_ENCODING': 'utf-8'
    })
process.crawl(TencentHomeSpider)
process.start()