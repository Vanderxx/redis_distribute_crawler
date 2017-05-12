# -*- coding: utf-8 -*-

import redis

REDIS_CLS = redis.StrictRedis
REDIS_HOST = "192.168.1.76"
REDIS_PORT = 6379
DUPEFILTER_QUEUE_KEY = "dupefilter:requests_seen"


REQUESTS_QUEUE_KEY = "tasks:backlog_requests"

