import scrapy
import json
from scrapy.crawler import CrawlerProcess
import common_utils.check as check

# $('.layout.mt12>.layoutLeft>div>div:not(.hd) a[href$=html]')
# $('.contentLayout .bd a[href$=html]')


class TencentHomeSpider(scrapy.Spider):
    name = "tencent_home"
    download_delay = 0

    def __init__(self):
        super(TencentHomeSpider, self).__init__()
        self.__urls = [
            'http://www.qq.com/',
        ]
        self.__module_urls = [
            'http://www.qq.com/ninja/newsBeijingContent_public.htm',
            'http://www.qq.com/ninja/houseQuanguoContent_public.htm',
            'http://www.qq.com/ninja/liveBeijing_NOINCLUDE_WITHOUTPULL.htm',
            'http://www.qq.com/ninja/meishiBeijing_NOINCLUDE_WITHOUTPULL.htm'
        ]

    def start_requests(self):
        for url in self.__urls:
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 meta={'dont_merge_cookies': True})
        for url in self.__module_urls:
            yield scrapy.Request(url=url,
                                 callback=self.parseModule,
                                 meta={'dont_merge_cookies': True})                         

    def parse(self, response):
        top = response.css('.layout.mt12>.layoutLeft>div>div:not(.hd)')
        bottom = response.css(('.contentLayout .bd'))
        news = []
        news.append(self.getNews(top))
        news.append(self.getNews(bottom))
        print(news)
        with open('tencent.log','a+') as f:
            f.write(json.dumps(news))
    
    def parseModule(self, response):
        body = response.css('*:not(.hd) a[href]')
        news = []
        news.append(self.getNews(body))
        print(news)
        with open('tencent.log','a+') as f:
            f.write(json.dumps(news))

    def getNews(self, selector):
        result = []
        cssSelector = ['a[href]']
        for each in cssSelector:
            for element in selector.css(each):
                title = element.css("::text").extract_first()
                link = element.css("::attr(href)").extract_first()
                if check.checkTitle(title) and check.checkLink(link):
                    dic = {
                        'title': title,
                        'link': link
                    }
                    result.append(dic)
        return result

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    # 'ITEM_PIPELINES': '{"pipeline.UrlPushPipeline.UrlPushPipeline": 300}',
    # 'REDIS_URI': '13.231.182.153',
    # 'REDIS_PASSWORD': 'redisredis',
    # 'REDIS_PORT': '6379',
    # 'REDIS_QUEUE_KEY': 'queue',
    # 'FEED_EXPORT_ENCODING': 'utf-8'
})
process.crawl(TencentHomeSpider)
process.start()
