import scrapy
from scrapy.crawler import CrawlerProcess
import common_utils.system_util as su
import time
import common_utils.time_util as tu

class TestPageSpider(scrapy.Spider):

    name = 'test_page'

    handle_httpstatus_list = [404, 500]

    def start_requests(self):
        yield scrapy.Request(url='http://news.163.com/18/0619/10/DKLI69TG0001875P.html',
                             callback=self.parse,
                             meta={'dont_merge_cookies': True})

    def parse_content(self, response):

        #抓所有h1，最长的认为是题目
        titles = []
        for title_pom in response.css('h1'):
            title = title_pom.css('::text').extract()
            for t in title:
                titles.append(t)

        if (len(titles) == 0):
            for title_pom in response.css('h2'):
                title = title_pom.css('::text').extract()
                for t in title:
                    titles.append(t)

        if (len(titles) == 0):
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
            'source': 'test',
            'date': date_now,
            'unix_timestamp': tu.datetime2timestamp(datetime_now)
        }
        return dict


    def parse(self, response):
        dict = self.parse_content(response)
        yield dict

process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'DOWNLOAD_DELAY': '1',
        'DOWNLOAD_TIMEOUT': 5
})
process.crawl(TestPageSpider)
process.start()