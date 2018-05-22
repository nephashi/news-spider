import scrapy
import common_utils.json_util as ju

class SohuGameSpider(scrapy.Spider):
    name = 'sohu_game'
    download_delay = 1

    base_url = "http://v2.sohu.com/public-api/feed"
    fixed_param = {'scene': 'CHANNEL',
                   'sceneId': 42}

    max_page = 99
    page_size = 20

    def start_requests(self):
        for page_idx in range(1, self.max_page + 1):
            url = self.base_url + "?"
            for key, value in self.fixed_param.items():
                url += (key + "=" + str(value))
                url += "&"
            url += "page=" + str(page_idx)
            url += "&"
            url += "size=" + str(self.page_size)
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 meta={'dont_merge_cookies': True})

    def parse(self, response):
        if (response.status == 200):
            json = response.body.decode('utf-8')
            data = ju.json2py(json)
            for item in data:
                news_dic = {
                    'title': item['title'],
                    'link': item['originalSource'],
                    'source': self.name
                }
                yield news_dic