import scrapy

class TestSpider(scrapy.Spider):

    name = 'test'

    def start_requests(self):
        yield scrapy.Request(url='null',
                             callback=self.parse,
                             meta={'dont_merge_cookies': True})

    def parse(self, response):
        print(response.body.decode('utf-8'))