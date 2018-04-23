from scrapy.crawler import CrawlerProcess
from spider.page_spider.PageSpider import PageSpider

def launch_crawl_news():
    process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'ITEM_PIPELINES': '{"pipeline.NewsPipeline.NewsPipeline": 300}',
        'REDIS_URI': '13.231.182.153',
        'REDIS_PASSWORD': 'redisredis',
        'REDIS_PORT': '6379',
        'REDIS_QUEUE_KEY': 'queue',
        'FEED_EXPORT_ENCODING': 'utf-8'
    })
    process.crawl(PageSpider)
    process.start()
    print("end")

launch_crawl_news()