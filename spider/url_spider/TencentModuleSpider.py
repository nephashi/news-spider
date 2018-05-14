import scrapy
import common_utils.check as check

class TencentModuleSpider(scrapy.Spider):
    name = "tencent_module"
    download_delay = 0

    def __init__(self):
        super(TencentModuleSpider, self).__init__()
        self.__module_urls = [
            'http://www.qq.com/ninja/newsBeijingContent_public.htm',
            'http://www.qq.com/ninja/houseQuanguoContent_public.htm',
            'http://www.qq.com/ninja/liveBeijing_NOINCLUDE_WITHOUTPULL.htm',
            'http://www.qq.com/ninja/meishiBeijing_NOINCLUDE_WITHOUTPULL.htm'
        ]

    def start_requests(self):
        for url in self.__module_urls:
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 meta={'dont_merge_cookies': True})

    def parse(self, response):
        body = response.css('*:not(.hd) a[href]')
        news = self.getNews(body)
        for url_dic in news:
            yield url_dic

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
                        'link': link,
                        'source': self.name
                    }
                    result.append(dic)
        return result