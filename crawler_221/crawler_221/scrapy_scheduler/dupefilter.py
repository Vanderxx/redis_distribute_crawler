# -*- coding: utf-8 -*-

from scrapy.dupefilters import BaseDupeFilter
from defaults import *
from scrapy.utils.request import request_fingerprint


class RFPDupfilter(BaseDupeFilter):
    def __init__(self, server, key):
        self.server = server
        self.key = key

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    @classmethod
    def from_settings(cls, settings):
        host = settings.get("REDIS_HOST", REDIS_HOST)
        port = settings.get("REDIS_PORT", REDIS_PORT)
        password = settings.get("REDIS_AUTH", REDIS_AUTH)
        redis_cls = settings.get("REDIS_CLS", REDIS_CLS)
        server = redis_cls(host=host, port=port, db=1, password=password)

        dupefilter_key = settings.get("DUPEFILTER_KEY", DUPEFILTER_KEY)

        return cls(server, dupefilter_key)

    def request_seen(self, request):
        fp = request_fingerprint(request)
        return self.server.sadd(self.key, fp) == 0

    def close(self, reason):
        self.clear()

    def clear(self):
        self.server.delete(self.key)