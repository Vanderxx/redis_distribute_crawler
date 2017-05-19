# -*- coding: utf-8 -*-

from redis import StrictRedis

REDIS_CLS = StrictRedis
REDIS_HOST = "192.168.1.76"
REDIS_PORT = 6379
REDIS_AUTH = "279279"

DUPEFILTER_KEY = "dupefilter:requests_seen"
TODO_TASKS_KEY = "tasks_queue:todo_tasks"

SCHEDULER_PERSIST = False

SCHEDULER_QUEUE_CLASS = "crawler_221.scrapy_scheduler.queue.FifoQueue"
