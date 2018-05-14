import scrapy
import common_utils.check as check

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

    def parse(self, response):
        top = response.css('.layout.mt12>.layoutLeft>div>div:not(.hd)')
        bottom = response.css(('.contentLayout .bd'))
        news = []
        news.append(self.getNews(top))
        news.append(self.getNews(bottom))
        for part in news:
            for url_dic in part:
                yield url_dic

    def parseModule(self, response):
        body = response.css('*:not(.hd) a[href]')
        news = []
        news.append(self.getNews(body))

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
