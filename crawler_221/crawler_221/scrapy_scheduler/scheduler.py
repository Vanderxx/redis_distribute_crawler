# -*- coding: utf-8 -*-

from scrapy.utils.misc import load_object
from dupefilter import RFPDupfilter
from defaults import *


class Scheduler(object):
    def __init__(self, server, persist, queue_key, queue_cls, dupefilter_key):
        self.server = server
        self.persist = persist
        self.queue_key = queue_key
        self.queue_cls = queue_cls
        self.dupefilter_key = dupefilter_key

        self.queue = None
        self.spider = None
        self.df = None

    def __len__(self):
        return len(self.queue)

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        cls.stats = crawler.stats
        return cls.from_settings(settings)

    @classmethod
    def from_settings(cls, settings):
        host = settings.get("REDIS_HOST", REDIS_HOST)
        port = settings.get("REDIS_PORT", REDIS_PORT)
        password = settings.get("REDIS_AUTH", REDIS_AUTH)
        server_cls = settings.get("REDIS_CLS", REDIS_CLS)
        server = server_cls(host=host, port=port, db=1, password=password)

        persist = settings.get("TASKS_PERSIST", SCHEDULER_PERSIST)
        queue_key = settings.get("TODO_TASKS_KEY", TODO_TASKS_KEY)
        queue_cls = load_object(settings.get("SCHEDULER_QUEUE_CLASS", SCHEDULER_QUEUE_CLASS))
        dupefilter_key = settings.get("DUPEFILTER_KEY", DUPEFILTER_KEY)

        return cls(server=server, persist=persist, queue_key=queue_key, queue_cls=queue_cls, dupefilter_key=dupefilter_key)

    def open(self, spider):
        self.spider = spider
        self.queue = self.queue_cls(server=self.server, key=self.queue_key, spider=spider)
        self.df = RFPDupfilter(server=self.server, key=self.dupefilter_key)

    def close(self, reason):
        if not self.persist:
            self.df.clear()
            self.queue.clear()

    def enqueue_request(self, request):
        if not request.dont_filter and self.df.request_seen(request):
            return
        self.stats.inc_value('scheduler/enqueued/redis', spider=self.spider)
        self.queue.push(request)

    def next_request(self):
        request = self.queue.pop()
        if request:
            self.stats.inc_value('scheduler/dequeued/redis', spider=self.spider)
        return request

    def has_pending_requests(self):
        return len(self) > 0