import scrapy
import common_utils.system_util as su
import time
import common_utils.time_util as tu

class PageSpider(scrapy.Spider):
    name = "page"
    download_delay = 0
    handle_httpstatus_list = [404, 500]

    def __init__(self):
        super(PageSpider, self).__init__()
        self.__redis_puller = None

    def get_redis_puller(self):
        return self.__redis_puller

    def set_redis_puller(self, redis_puller):
        self.__redis_puller = redis_puller

    def start_requests(self):
        url = self.__redis_puller.get_url()
        if (url != None):
            yield scrapy.Request(url=url,
                        callback=self.parse,
                        meta={'dont_merge_cookies': True},
                        dont_filter=True)
        else:
            self.logger.info("url queue empty, finish.")

    def parse_content(self, response):
        line_break = su.get_line_break()

        #抓所有h1，最长的认为是题目
        titles = []
        for title_pom in response.css('h1'):
            title = title_pom.css('::text').extract_first()
            if(titles != None):
                titles.append(title)
        title = ""
        for t in titles:
            if (t != None and len(t) > len(title)):
                title = t

        #抓所有p，连起来认为是内容
        content = ""
        for p_pom in response.css('p'):
            parag = p_pom.css('::text').extract_first()
            if (parag != None and len(parag.strip()) > 0):
                content += parag
                content += line_break
        date_now = time.strftime("%Y-%m-%d", time.localtime())
        dict = {
            'title': title,
            'link': response.url,
            'content': content,
            'date': date_now,
            'unix_timestamp': tu.date2timestamp(date_now)
        }
        return dict

    def parse(self, response):
        if (response.status == 200):
            dict = self.parse_content(response)
            yield dict

        url = self.__redis_puller.get_url()
        if (url != None):
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 meta={'dont_merge_cookies': True},
                                 dont_filter=True)
        else:
            self.logger.info("url queue empty, finish.")