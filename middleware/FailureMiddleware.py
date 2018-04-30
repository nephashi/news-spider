import scrapy

class FailureMiddleware(object):

    def process_exception(self, request, exception, spider):
        spider.logger.info("catch Exception: " + str(exception))
        rup = spider.get_redis_puller()
        url = rup.get_url()
        if (url != None):
            return scrapy.Request(url=url,
                                 callback=spider.parse,
                                 meta={'dont_merge_cookies': True},
                                 dont_filter=True)