import scrapy
import common_utils.json_util as ju

class WangYiFinanceSpider(scrapy.Spider):
    name = "163_finance"

    finance_url_pre = [
        'http://money.163.com/special/002557S5/newsdata_idx_index.js',
        'http://temp.163.com/special/00804KVA/cm_money'
    ]

    finance_url_aft = '.js'

    def __init__(self):
        super(WangYiFinanceSpider, self).__init__()

    def start_requests(self):
        for pre in self.finance_url_pre:
            for aft in range(1, 11):
                if (aft == 1):
                    yield scrapy.Request(url=pre + self.finance_url_aft,
                                         callback=self.parse,
                                         meta={'dont_merge_cookies': True}
                                         )
                elif (aft < 10):
                    yield scrapy.Request(url = pre + '_0' + str(aft) + self.finance_url_aft,
                                     callback=self.parse,
                                     meta={'dont_merge_cookies': True}
                                     )
                else:
                    yield scrapy.Request(url=pre + '_' + str(aft) + self.finance_url_aft,
                                         callback=self.parse,
                                         meta={'dont_merge_cookies': True}
                                         )

    def parse(self, response):
        if (response.status == 200):
            decode_flag = True
            json = ''
            try:
                json = response.body.decode('gbk')[14:-1]
            except Exception as e:
                print(e)
                decode_flag = False
            if (decode_flag == True):
                data = ju.json2py(json)
                for item in data:
                    news_dic = {
                        'title': item['title'],
                        'link': item['docurl'],
                        'source': self.name
                    }
                    yield news_dic