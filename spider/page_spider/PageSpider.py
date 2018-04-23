import scrapy
import common_utils.system_util as su

class PageSpider(scrapy.Spider):
    name = "page"
    download_delay = 0

    def __init__(self):
        super(PageSpider, self).__init__()
        self.__redis_puller = None


    def set_redis_puller(self, redis_puller):
        self.__redis_puller = redis_puller

    def start_requests(self):
        url = self.__redis_puller.get_url()
        if (url != None):
            yield scrapy.Request(url=url,
                        callback=self.parse,
                        meta={'dont_merge_cookies': True},
                        dont_filter=True)

    def parse_content(self, response):
        line_break = su.get_line_break()

        titles = []
        for title_pom in response.css('h1'):
            title = title_pom.css('::text').extract_first()
            if(titles != None):
                titles.append(title)
        content = ""
        for p_pom in response.css('p'):
            parag = p_pom.css('::text').extract_first()
            if (parag != None and len(parag.strip()) > 0):
                content += parag
                content += line_break
        dict = {
            'title': titles,
            'content': content
        }
        return dict

    def parse(self, response):
        dict = self.parse_content(response)

        yield dict

        url = self.__redis_puller.get_url()
        if (url != None):
            yield scrapy.Request(url=url,
                                 callback=self.parse,
                                 meta={'dont_merge_cookies': True},
                                 dont_filter=True)