import scrapy
import common_utils.json_util as ju

class WangYiYaoWenSpider(scrapy.Spider):
    name = "163_yaowen"

    yaowen_url_pre = 'http://temp.163.com/special/00804KVA/cm_yaowen'
    yaowen_url_aft = '.js'

    handle_httpstatus_list = [404, 500]

    def __init__(self):
        super(WangYiYaoWenSpider, self).__init__()
        self.__page = 2

    def start_requests(self):
        yield scrapy.Request(url = self.yaowen_url_pre + self.yaowen_url_aft,
                             callback = self.parse,
                             meta = {'dont_merge_cookies': True})

    def parse(self, response):
        if (response.status == 200):
            json = response.body.decode('gbk')[14:-1]
            data = ju.json2py(json)
            for item in data:
                news_dic = {
                    'title': item['title'],
                    'link': item['docurl'],
                    'source': self.name
                }
                yield news_dic

            if (self.__page < 10):
                yield scrapy.Request(url = self.yaowen_url_pre + '_0' + str(self.__page) + self.yaowen_url_aft,
                                     callback=self.parse,
                                     meta={'dont_merge_cookies': True}
                                     )
            else:
                yield scrapy.Request(url = self.yaowen_url_pre + '_' + str(self.__page) + self.yaowen_url_aft,
                                     callback=self.parse,
                                     meta={'dont_merge_cookies': True}
                                     )
            self.__page += 1