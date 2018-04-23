from scrapy.crawler import CrawlerProcess
from spider.url_spider.SinaHomeSpider import SinaHomeSpider

def launch_crawl_single_homepage_for_url(spider_cls):
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'ITEM_PIPELINES': '{"pipeline.UrlPushPipeline.UrlPushPipeline": 300}',
        'REDIS_URI': '13.231.182.153',
        'REDIS_PASSWORD': 'redisredis',
        'REDIS_PORT': '6379',
        'REDIS_QUEUE_KEY': 'queue',
        'FEED_EXPORT_ENCODING': 'utf-8'
    })
    process.crawl(spider_cls)
    process.start()
    print("end")

launch_crawl_single_homepage_for_url(SinaHomeSpider)