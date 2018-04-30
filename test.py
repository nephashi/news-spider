from scrapy.crawler import Crawler
from scrapy.conf import settings
from spider.page_spider import PageSpider
from scrapy import log, project
from twisted.internet import reactor
from billiard import Process
from scrapy.utils.project import get_project_settings

class UrlCrawlerScript(Process):
    def __init__(self, spider):
        Process.__init__(self)
        settings = get_project_settings()
        self.crawler = Crawler(settings)
        self.crawler.configure()
        self.crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
        self.spider = spider

    def run(self):
        self.crawler.crawl(self.spider)
        self.crawler.start()
        reactor.run()

def run_spider(url):
    spider = MySpider(url)
    crawler = UrlCrawlerScript(spider)
    crawler.start()
    crawler.join()