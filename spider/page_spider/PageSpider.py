import scrapy
import common_utils.system_util as su
import time
import common_utils.time_util as tu

class PageSpider(scrapy.Spider):
    name = "page"
    download_delay = 2
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

        url_item = self.__redis_puller.get_last_pulled_item()
        if (url_item != None):
            source = url_item['source']
        else:
            source = "unknown"

        #抓所有h1，最长的认为是题目
        titles = []
        for title_pom in response.css('h1'):
            title = title_pom.css('::text').extract()
            for t in title:
                titles.append(t)

        for title_pom in response.css('h2'):
            title = title_pom.css('::text').extract()
            for t in title:
                titles.append(t)

        for title_pom in response.css('h3'):
            title = title_pom.css('::text').extract()
            for t in title:
                titles.append(t)

        title = ""
        for t in titles:
            if (t.strip() != None and len(t.strip()) > len(title)):
                title = t.strip()

        # 题目太长，很可能抓到了代码，只留下中文
        if (len(title) > 100):
            title_cp = title
            title = ""
            for c in title_cp:
                if ('\u4e00' <= c <= '\u9fff'):
                    title += c

        #抓所有p，连起来认为是内容
        content = ""
        for p_pom in response.css('p'):
            parag_slices = p_pom.css('::text').extract()
            for parag in parag_slices:
                if (parag != None and len(parag.strip()) > 0):
                    content += parag
                    content += '\r\n'

        datetime_now = time.strftime("%Y-%m-%d,%H:%M:%S", time.localtime())
        date_now = time.strftime("%Y-%m-%d", time.localtime())
        dict = {
            'title': title,
            'link': response.url,
            'content': content,
            'source': source,
            'date': date_now,
            'unix_timestamp': tu.datetime2timestamp(datetime_now)
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