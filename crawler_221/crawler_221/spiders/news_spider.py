# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.spidermiddlewares.httperror import HttpError


class NewsSpider(Spider):
    name = "news_spider"

    def parse(self, response):
        print response.status
        selector = Selector(response)
        title_name = selector.xpath("/html/head/title/text()").extract()[0]
        print title_name

    def errback(self, failure):
        self.logger.error("Error: http status: %s" % failure.value.response.status)

        # retry_times = failure.request.meta['retry_times']
        # if retry_times >= 1:
        #     retry_times -= 1
        #     self.crawler.engine.schedule(failure.request, self)


