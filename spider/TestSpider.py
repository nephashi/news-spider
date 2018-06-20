import scrapy
from scrapy.crawler import CrawlerProcess
import common_utils.time_util as tu
import time
from spider.url_spider.WangYiYaoWenSpider import WangYiYaoWenSpider
from spider.url_spider.WangYiSportSpider import WangYiSportSpider
from spider.url_spider.WangYiEntertainmentSpider import WangYiEntertainmentSpider
from spider.url_spider.WangYiFinanceSpider import WangYiFinanceSpider
from spider.url_spider.WangYiBeijingSpider import WangYiBeijingSpider
from spider.url_spider.WangYiTechSpider import WangYiTechSpider
from spider.url_spider.WangYiDomesticSpider import WangYiDomesticSpider
from spider.url_spider.WangYiInternationalSpider import WangYiInternationalSpider
from spider.url_spider.WangYiAutoSpider import WangYiAutoSpider
from spider.url_spider.WangYiMilitarySpider import WangYiMilitarySpider
import chardet

class TestSpider(scrapy.Spider):

    name = 'test'

    handle_httpstatus_list = [404, 500]

    def start_requests(self):
        yield scrapy.Request(url='http://sports.163.com/special/000587PR/newsdata_n_index.js',
                             callback=self.parse,
                             meta={'dont_merge_cookies': True})


    def parse(self, response):
        bytes = response.body
        print(chardet.detect(bytes))
        #content = bytes.decode('GB2312')
        #print(content)


process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'DOWNLOAD_DELAY': '1',
        'DOWNLOAD_TIMEOUT': 30
})
process.crawl(WangYiMilitarySpider)
process.start()