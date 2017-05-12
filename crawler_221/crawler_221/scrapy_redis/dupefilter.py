# -*-coding:utf-8-*-


from scrapy.dupefilter import BaseDupeFilter
from scrapy.utils.request import request_fingerprint
from redis_default import REDIS_CLS, REDIS_HOST, REDIS_PORT, DUPEFILTER_QUEUE_KEY


class RFPDupeFilter(BaseDupeFilter):

    def __init__(self, server, key):
        self.server = server
        self.key = key

    @classmethod
    def from_settings(cls, settings):
        host = settings.get('REDIS_HOST', REDIS_HOST)
        port = settings.get('REDIS_PORT', REDIS_PORT)
        server = REDIS_CLS(host, port)
        key = settings.get("DUPEFILTER_KEY", DUPEFILTER_QUEUE_KEY)
        return cls(server, key)

    @classmethod
    def from_crawler(cls, crawler):
        return cls.from_settings(crawler.settings)

    def request_seen(self, request):

        fp = request_fingerprint(request)
        added = self.server.sadd(self.key, fp)
        return added == 0

    def close(self, reason):
        """Delete data on close. Called by scrapy's scheduler"""
        self.clear()

    def clear(self):
        """Clears fingerprints data"""
        self.server.delete(self.key)
