from scrapy.crawler import CrawlerProcess
from spider.url_spider.SohuPoliticsSpider import SohuPoliticsSpider
from spider.url_spider.SohuInternationalSpider import SohuInternationalSpider
from spider.url_spider.SohuFashionSpider import SohuFashionSpider
from spider.url_spider.SohuMilitarySpider import SohuMilitarySpider
from spider.url_spider.SohuTechnologySpider import SohuTechnologySpider
from spider.url_spider.SohuFinanceSpider import SohuFinanceSpider
from spider.url_spider.SohuGameSpider import SohuGameSpider
from spider.url_spider.SohuAnimationSpider import SohuAnimationSpider
from spider.url_spider.SohuEntertainmentSpider import SohuEntertainmentSpider
from spider.url_spider.SohuSportSpider import SohuSportSpider
from spider.TestSpider import TestSpider

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
    })
process.crawl(SohuFashionSpider)
process.start()