import scrapy
import common_utils.json_util as ju

class SohuEntertainmentSpider(scrapy.Spider):
    name = 'sohu_entertainment'

    url = 'http://yule.sohu.com/_scroll_newslist/20180521/news.inc'

    def start_requests(self):
        yield scrapy.Request(url=self.url,
                                 callback=self.parse,
                                 meta={'dont_merge_cookies': True})

    def parse(self, response):
        if (response.status == 200):
            json = response.body.decode('utf-8')[16:].replace('category', '"category"').replace('item', '"item"')

            newses = ju.json2py(json)['item']
            for n in newses:
                news_dic = {
                    'title': n[1],
                    'link': n[2],
                    'source': self.name
                }
                yield news_dic