# -*- coding: utf-8 -*-

from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.http.request import Request
from scrapy.spidermiddlewares.httperror import HttpError


class NewsSpider(Spider):
    name = "news_spider"
    start_urls = [
        "https://book.douban.com/tag/",
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield Request(url=url,
                          callback=self.parse,
                          errback=self.errback,
                          headers={
                              "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87"
                          },
                          dont_filter=True,
                          )

    def parse(self, response):
        selector = Selector(response)
        title_name = selector.xpath("/html/head/title/text()").extract()[0]
        print title_name

    def errback(self, failure):
        if isinstance(failure.value, HttpError):
            self.logger.error("HttpError: %s" % failure.value.response.status)
        else:
            self.logger.error("Error: %r" % failure)
