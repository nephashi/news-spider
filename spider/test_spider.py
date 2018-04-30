import scrapy
import scrapy.crawler as crawler
from multiprocessing import Process, Queue
from twisted.internet import reactor

# your spider
class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com/tag/humor/']

    def parse(self, response):
        for quote in response.css('div.quote'):
            print(quote.css('span.text::text').extract_first())


# the wrapper to make it run more times
def run_spider():
    def f(q):
        try:
            runner = crawler.CrawlerRunner()
            deferred = runner.crawl(QuotesSpider)
            deferred.addBoth(lambda _: reactor.stop())
            reactor.run()
            q.put(None)
        except Exception as e:
            q.put(e)

    q = Queue()
    p = Process(target=f, args=(q,))
    p.start()
    result = q.get()
    p.join()

    if result is not None:
        raise result


print('first run:')
run_spider()

print('\nsecond run:')
run_spider()