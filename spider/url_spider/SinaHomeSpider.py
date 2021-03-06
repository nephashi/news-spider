import scrapy

class SinaHomeSpider(scrapy.Spider):
    name = "sina_home"
    #download_delay = 10

    sina_url = 'http://www.sina.com.cn/'

    def __init__(self):
        super(SinaHomeSpider, self).__init__()
        self.__urls = [
            self.sina_url
        ]

    def start_requests(self):
        for url in self.__urls:
            yield scrapy.Request(url = url,
                                 callback = self.parse,
                                 meta = {'dont_merge_cookies': True})

    def parse(self, response):
        for i in range(97, 123):
            for news in response.css('.list-' + chr(i)\
                    + '>li>a[href]'):
                news_dic = {
                    'title': news.css('::text').extract_first(),
                    'link': news.css('::attr(href)').extract_first(),
                    'source': self.name
                }
                yield news_dic


