import scrapy
from scrapy.crawler import CrawlerProcess
import common_utils.time_util as tu
import time

class TestSpider(scrapy.Spider):

    name = 'test'

    def start_requests(self):
        yield scrapy.Request(url='https://mp.weixin.qq.com/s/ZBvUiGKCD7ScoqI3syn8iw',
                             callback=self.parse,
                             meta={'dont_merge_cookies': True})

    def parse_content(self, response):
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

        date_now = time.strftime("%Y-%m-%d,%H:%M:%S", time.localtime())
        dict = {
            'title': title,
            'link': response.url,
            'content': content,
            'source': source,
            'date': date_now,
            'unix_timestamp': tu.datetime2timestamp(date_now)
        }
        return dict

    def parse(self, response):
        if (response.status == 200):
            dict = self.parse_content(response)
            yield dict

process = CrawlerProcess({
        'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
        'DOWNLOAD_DELAY': '1',
        'DOWNLOAD_TIMEOUT': 5
})
process.crawl(TestSpider)
process.start()