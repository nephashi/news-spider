from scrapy.crawler import CrawlerProcess
from spider.page_spider.PageSpider import PageSpider
import sys

# 这里只能执行一次爬虫，要不停爬要执行launch_news_loop.py
sys.stderr = sys.stdout

def launch_crawl_news():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'ITEM_PIPELINES': '{"pipeline.NewsPipeline.NewsPipeline": 300}',
        'DOWNLOADER_MIDDLEWARES': '{"middleware.FailureMiddleware.FailureMiddleware": 0}',
        'DOWNLOAD_DELAY': '1',
        'REDIS_URI': '13.231.182.153',
        'REDIS_PASSWORD': 'redisredis',
        'REDIS_PORT': '6379',
        'REDIS_QUEUE_KEY': 'queue',
        'MGDB_URI': '18.182.13.109',
        'MGDB_PORT': '27017',
        'MGDB_DB_NAME': 'news_db',
        'FEED_EXPORT_ENCODING': 'utf-8',
        'LOG_FILE': '../logs/NewsSpider.log',
        'LOG_ENCODING': 'utf-8'
    })
    process.crawl(PageSpider)
    process.start()

launch_crawl_news()