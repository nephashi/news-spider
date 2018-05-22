import scrapy

class SohuSportSpider(scrapy.Spider):
    name = 'sohu_sport'

    url = 'http://sports.sohu.com/'

    def start_requests(self):
        yield scrapy.Request(url = self.url,
                             callback = self.parse,
                             meta = {'dont_merge_cookies': True})

    def parse(self, response):
        css_selector_p = ['.blockCA p>a[href]']
        css_selector_li = ['.blockCB li>a[href]',
                           '.blockLA li>a[href]', '.blockLB li>a[href]', '.blockLC li>a[href]',
                           '.blockLD li>a[href]', '.blockLE li>a[href]',]
        for selector in (css_selector_p + css_selector_li):
            for news in response.css(selector):
                news_dic = {
                    'title': news.css('::text').extract_first(),
                    'link': news.css('::attr(href)').extract_first(),
                    'source': self.name
                }
                yield news_dic